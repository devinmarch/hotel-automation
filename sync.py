import os
import json
import requests
from db import Reservations
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

days_behind = 7
days_ahead = 7

check_in_from = (datetime.now() - timedelta(days=days_behind)).strftime('%Y-%m-%d')
check_in_to = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

room_type_id = '537928'

def sync():
    
    reservations = requests.get(
        f'https://api.cloudbeds.com/api/v1.3/getReservations',
        headers={'Authorization': f'Bearer {os.environ["CLOUDBEDS_API_KEY"]}'},
        params={
            'propertyID': f'{os.environ["CLOUDBEDS_PROPERTY_ID"]}',
            'checkInFrom': f'{check_in_from}',
            'checkInTo': f'{check_in_to}',
            'roomTypeID': f'{room_type_id}'

        }
    ).json()

    returned_ids = [r['reservationID'] for r in reservations['data']]

    for r in reservations['data']:
        res, created = Reservations.get_or_create(
            reservation_id=r['reservationID'],
            defaults={
                'date_modified': r['dateModified'],
                'status': r['status'],
                'guest_name': r['guestName'],
                'start_date': r['startDate'],
                'end_date': r['endDate'],
                'balance': r['balance'],
            }
        )

        if not created:
            Reservations.update(
            date_modified=r['dateModified'],
            status=r['status'],
            guest_name=r['guestName'],
            start_date=r['startDate'],
            end_date=r['endDate'],
            balance=r['balance'],
        ).where(Reservations.reservation_id == r['reservationID']).execute()
    
    Reservations.delete().where(Reservations.reservation_id.not_in(returned_ids)).execute()


    assignments = requests.get(
        'https://api.cloudbeds.com/api/v1.3/getReservationsWithRateDetails',
        headers={'Authorization': f'Bearer {os.environ["CLOUDBEDS_API_KEY"]}'},
        params={
            'propertyID': os.environ['CLOUDBEDS_PROPERTY_ID'],
            'reservationID': ','.join(returned_ids),
        }
    ).json()

    all_room_keys = []

    for reservation in assignments['data']:
        res_id = str(reservation['reservationID'])
        for room in reservation['rooms']:
            room_id = room['roomID'] or ''
            all_room_keys.append(room_id)

            assignment, created = Assignments.get_or_create(
                reservation_id=res_id,
                room_id=room_id,
                defaults={
                    'room_type_name': room['roomTypeName'],
                    'guest_name': room['guestName'],
                    'room_check_in': room['roomCheckIn'],
                    'room_check_out': room['roomCheckOut'],
                    'room_status': room['roomStatus'],
                }
             )
            
            if not created:
                Assignments.update(
                    room_type_name=room['roomTypeName'],
                    guest_name=room['guestName'],
                    room_check_in=room['roomCheckIn'],
                    room_check_out=room['roomCheckOut'],
                    room_status=room['roomStatus'],
            ).where(
                (Assignments.reservation_id == str(res_id)) &
                (Assignments.room_id == room_id)
            ).execute()
    
    Assignments.delete().where(
        Assignments.reservation_id.not_in(returned_ids)
    ).execute()

if __name__ == '__main__':
    sync()