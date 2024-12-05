from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler


client_id = 'cc68db0bcbf14ddcbc5f1a742c3ea215'
client_secret = 'b37f65f0812e45a398bde333da674671'
scope = 'user-top-read'

redirect_url = 'http://127.0.0.1:5000/spotify/callback'

def create_spotify_instance(session):
    cache_handler = FlaskSessionCacheHandler(session)
    sp_oauth = SpotifyOAuth(
        client_id= 'cc68db0bcbf14ddcbc5f1a742c3ea215',
        client_secret='b37f65f0812e45a398bde333da674671',
        redirect_uri= redirect_url,
        scope="user-top-read",
        cache_handler=cache_handler
    )
    sp = Spotify(auth_manager=sp_oauth) 
    return sp

def get_user_top_items(session, item_type = 'artist', limit = 10, time_range = 'medium_term'):
    try:
        sp = create_spotify_instance(session)
        if item_type == 'artists':
            return sp.current_user_top_artists(limit=limit, time_range=time_range)['items']
        elif item_type == 'tracks':
            return sp.current_user_top_tracks(limit=limit, time_range=time_range)['items']
        else:
            raise ValueError("Invalid item_type. Choose 'artists' or 'tracks'.")
    except Exception as e:
        print(f"Error fetching top {item_type}: {str(e)}")
        return []


