# Sample CloudBeds API request formats

# CloudBeds POST request
response = requests.post(
        f'https://api.cloudbeds.com/api/v1.3/{method}',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'propertyID': f'{propertyID}',
            'object': f'{eventObject}',
            'action': f'{eventAction}',
            'endpointUrl': f'{endpointUrl}'
        }
    )


# CloudBeds GET request
response = requests.get(
        f'https://api.cloudbeds.com/api/v1.3/{method}',
        headers={'Authorization': f'Bearer {API_KEY}'},
        data={
            'propertyID': f'{propertyID}',
        }
    )

#CloudBeds DELETE request
response = requests.delete(
        f'https://api.cloudbeds.com/api/v1.3/{method}',
        headers={'Authorization': f'Bearer {API_KEY}'},
        params={
            'propertyIDs': f'{propertyID}',
            'subscriptionID': f'{webhookId}'
        }
    )