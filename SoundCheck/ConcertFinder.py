import requests
import math
from Concert import Concert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///app.db')
Session = sessionmaker(bind=engine)
session = Session()

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
def compileConcerts():


    url = 'https://app.ticketmaster.com/discovery/v2/events.json'


    api_key = 'GWiMxKfIqtPFeOYwdlQnGIYzTVVOeqgz'
      
    userCity = "Atlanta"

    params = {
        'apikey': api_key,
        'keyword': 'concert',
        'city': userCity,
        'countryCode': 'US',
        'size': 100
    }

# Send the GET request
    response = requests.get(url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
    # Parse the JSON data
        data = response.json()
    
    # Access events data
        events = data.get('_embedded', {}).get('events', [])
        
        unique_events = set()

        for event in events:
            artist = event.get('name')
            venue = event['_embedded']['venues'][0]
            venue_name = venue.get('name')
            venue_address = venue.get('address').get('line1','N/A')
            event_date = event.get('dates').get('start').get('localDate')
            
            event_key = (artist, venue_name, venue_address)

            if event_key not in unique_events and not any(keyword in event_key[0] for keyword in ["Test", "M&G", "VIP"]):
                unique_events.add(event_key)
                concert = Concert(artist,venue_name,event_date)
                concert.add_concert(session)
def getAllConcerts():
    concerts = session.query(Concert).all()
    for concert in concerts:
        details = concert.display_concert_details()
        return details
compileConcerts()
getAllConcerts()



   

    
    
