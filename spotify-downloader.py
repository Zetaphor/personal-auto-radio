import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Create or define the Music directory
music_directory = os.path.join(script_directory, "Music")
os.makedirs(music_directory, exist_ok=True)

def parse_spotify_item(url):
    # Determine whether the URL is an album or playlist
    url_type = url.split('/')[-2]

    # Extract the ID from the URL
    id = url.split('/')[-1].split('?')[0]

    # Authenticate with the Spotify API using client credentials
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get the details from the API
    if url_type == "album":
        album = sp.album(id)
        artist = album['artists'][0]['name']
        album_name = album['name']
        return [(artist, album_name, id, url_type)] # Returns album id for albums
    elif url_type == "playlist":
        playlist = sp.playlist(id)
        return [(track['track']['artists'][0]['name'], track['track']['album']['name'], track['track']['id'], url_type) for track in playlist['tracks']['items']]
    else:
        raise ValueError("URL must be an album or playlist")

# Read the file containing the list of URLs
file_path = os.path.join(script_directory, 'urls.txt')
with open(file_path, 'r') as file:
    urls = file.read().splitlines()

# Process each URL
for url in urls:
    items = parse_spotify_item(url)

    for artist, album_name, id, url_type in items:
        # Create the artist folder inside the Music folder
        artist_folder = os.path.join(music_directory, artist)
        os.makedirs(artist_folder, exist_ok=True)

        # Create the album folder inside the artist folder
        album_folder = os.path.join(artist_folder, album_name)
        os.makedirs(album_folder, exist_ok=True)

        # Run a bash command inside the album folder
        os.chdir(album_folder)

        # if album, download album once, if playlist, download tracks
        if url_type == "album":
            os.system(f"spotdl download 'https://open.spotify.com/album/{id}'")  # Download the entire album
        else:
            os.system(f"spotdl download 'https://open.spotify.com/track/{id}'")  # Download specific track

        # Move back to the Music directory after each iteration
        os.chdir(music_directory)
