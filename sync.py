import os
import json
import requests
from db import Reservations, Assignments
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

days_behind = 7
days_ahead = 7

check_in_from = (datetime.now() - timedelta(days=days_behind)).strftime('%Y-%m-%d')
check_in_to = (datetime.now() + timedelta(days=days_ahead)).strftime('%Y-%m-%d')

room_type_id = '537928'

inactive_statuses = ['checked_out', 'canceled', 'no_show', 'not_confirmed']


def _json_or_text(response):
    try:
        return response.json()
    except ValueError:
        print(f'Bad response {response.text}')
        return None
    

def sync():
    
    response = requests.get(
        f'https://api.cloudbeds.com/api/v1.3/getReservations',
        headers={'Authorization': f'Bearer {os.environ["CLOUDBEDS_API_KEY"]}'},
        params={
            'propertyID': f'{os.environ["CLOUDBEDS_PROPERTY_ID"]}',
            'checkInFrom': f'{check_in_from}',
            'checkInTo': f'{check_in_to}',
            'roomTypeID': f'{room_type_id}'

        }
    )

    reservations = _json_or_text(response)
    reservation_ids_comma = ','.join(str(r['reservationID']) for r in reservations['data'])

    response = requests.get(
        f'https://api.cloudbeds.com/api/v1.3/getReservationsWithRateDetails',
        headers={'Authorization': f'Bearer {os.environ["CLOUDBEDS_API_KEY"]}'},
        params={
            'propertyID': f'{os.environ["CLOUDBEDS_PROPERTY_ID"]}',
            'reservationID': f'{reservation_ids_comma}'
        }
    )

    reservations_detailed = _json_or_text(response)
    reservation_ids = [str(r['reservationID']) for r in reservations_detailed['data']]

    reservations = [
        {
            'reservation_id': res['reservationID'],
            'date_modified': res['dateModified'],
            'status': res['status'],
            'guest_name': res['guestName'],
            'start_date': res['reservationCheckIn'],
            'end_date': res['reservationCheckOut'],
            'balance': res['balance'],
        }
        for res in reservations_detailed['data']
    ]

    print(f'Found {len(reservations)} reservations')

    room_assignments = [
        {
            'reservation': res['reservationID'],
            'room_id': room['roomID'],
            'room_status': room['roomStatus'],
            'room_check_in': room['roomCheckIn'],
            'room_check_out': room['roomCheckOut'],
        }
        for res in reservations_detailed['data']
        if res['status'] not in inactive_statuses
        for room in res['rooms']
    ]

    print(f'Found {len(room_assignments)} assignments')

    Reservations.insert_many(reservations).on_conflict(
        conflict_target=[Reservations.reservation_id],
        preserve=[Reservations.date_modified,
                  Reservations.status,
                  Reservations.guest_name,
                  Reservations.start_date,
                  Reservations.end_date,
                  Reservations.balance]
    ).execute()

    deleted_reservations = Reservations.delete().where(
        Reservations.reservation_id.not_in(reservation_ids)
    ).execute()

    print(f'Deleted {deleted_reservations} record/s')

    Assignments.insert_many(room_assignments).on_conflict(
        conflict_target=[Assignments.reservation, Assignments.room_id],
        preserve=[Assignments.room_status,
                  Assignments.room_check_in,
                  Assignments.room_check_out]
    ).execute()

    Assignments.delete().where(
        Assignments.reservation.in_(
            Reservations.select().where(Reservations.status.in_(inactive_statuses))
        )
    ).execute()


if __name__ == '__main__':
    sync()