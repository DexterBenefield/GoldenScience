import requests
import math
def distanceFromMe(lat1, lon1, lat2, lon2):
    radius=3958.8
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in miles
    distance = radius * c
    return distance
def compileConcerts(eventlist, event):
    return eventlist.append(event)


url = 'https://app.ticketmaster.com/discovery/v2/events.json'


api_key = 'GWiMxKfIqtPFeOYwdlQnGIYzTVVOeqgz'  


params = {
    'apikey': api_key,
    'keyword': 'concert',         # Search for concerts
    'city': 'New York City',           # Example city
    'countryCode': 'US',          # Example country code
    'size': 3                    # Number of events to retrieve
}

# Send the GET request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = response.json()
    
    # Access events data
    events = data.get('_embedded', {}).get('events', [])
latUser = float(input('enter your latitude:'))
longUser = float(input('enter your longitude:'))




for event in events:
    venue = event['_embedded']['venues'][0]
    latEvent = venue['location']['latitude']
    longEvent = venue['location']['longitude']

    print(distanceFromMe(latUser, longUser, float(latEvent),float(longEvent)))
    print(latEvent, longEvent)
    print(venue)
    
    
