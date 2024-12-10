import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from dotenv import load_dotenv


load_dotenv()

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
scope = 'user-top-read'

redirect_url = 'http://127.0.0.1:5000/spotify/callback'

def create_spotify_instance(session, force_login=False):
    cache_handler = FlaskSessionCacheHandler(session)
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_url,
        scope=scope,
        cache_handler=cache_handler,
        show_dialog=True,  # Ensures the login dialog appears every time
    )
    sp = Spotify(auth_manager=sp_oauth)
    return sp

def get_user_top_items(session, item_type='artist', limit=50, time_range='long_term'):
    try:
        sp = create_spotify_instance(session)
        print(f"DEBUG: Fetching user's top {item_type} from Spotify...")
        if item_type == 'artists':
            top_artists = sp.current_user_top_artists(limit=limit, time_range=time_range)['items']
            print(f"DEBUG: Top artists retrieved: {[artist['name'] for artist in top_artists]}")
            return top_artists
        elif item_type == 'tracks':
            top_tracks = sp.current_user_top_tracks(limit=limit, time_range=time_range)['items']
            print(f"DEBUG: Top tracks retrieved: {[track['name'] for track in top_tracks]}")
            return top_tracks
        else:
            raise ValueError("Invalid item_type. Choose 'artists' or 'tracks'.")
    except Exception as e:
        print(f"ERROR: Could not fetch top {item_type} - {e}")
        return []
