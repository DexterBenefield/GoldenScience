import requests
import math
from Concert import Concert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()

TICKETMASTER_API_KEY = 'GWiMxKfIqtPFeOYwdlQnGIYzTVVOeqgz'

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
def compileConcerts(top_artists=None, exclude_keywords=None):
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'apikey': TICKETMASTER_API_KEY,
        'classificationName': 'music, concert,',
        'latlong': '33.7490,-84.3880',
        'radius': 50,
        'unit': 'miles',
        'size': 200
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching concerts from Ticketmaster: {response.status_code}")
        return []

    data = response.json()
    events = data.get('_embedded', {}).get('events', [])
    concerts = []
    exclude_keywords = exclude_keywords or ["Test", "M&G", "VIP", "Club"]

    print(f"Total events fetched from Ticketmaster: {len(events)}")
    for event in events:
        artist = event.get('name', '').lower()
        venue = event['_embedded']['venues'][0]
        venue_name = venue.get('name', 'Unknown Venue')
        url = event.get('url', '')

        event_date_str = event.get('dates', {}).get('start', {}).get('localDate')
        event_time_str = event.get('dates', {}).get('start', {}).get('localTime')
    
        if event_date_str and event_time_str:
            event_date = datetime.strptime(f"{event_date_str} {event_time_str}", "%Y-%m-%d %H:%M:%S")
        elif event_date_str:
            event_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        else:
            event_date = None

        if any(keyword.lower() in artist for keyword in exclude_keywords):
            print(f"Excluding event '{artist}' due to keyword match.")
            continue

        if top_artists and not any(top_artist in artist for top_artist in top_artists):
            continue

        concerts.append({
            'artist_name': artist.title(),
            'venue': venue_name,
            'date': event_date,
            'url': url,
        })
    concerts.sort(key=lambda x: x['date'] if x['date'] else datetime.max)
    print(f"Concerts after exclusions and sorting: {len(concerts)}")
    return concerts





   

    
    
