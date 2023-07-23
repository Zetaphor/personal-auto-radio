# This script loads a text file of Spotify share URLs (albums or playlists) and downloads them to MP3s using spotdl
# It automatically creates a folder for the artist, and then creates subfolders for each album

import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Load environment variables from .env file
load_dotenv()

# Get the absolute path of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Create or define the Albums directory
albums_directory = os.path.join(script_directory, "Albums")
os.makedirs(albums_directory, exist_ok=True)

def parse_spotify_album(url):
    # Extract the album ID from the URL
    album_id = url.split('/')[-1].split('?')[0]

    # Authenticate with the Spotify API using client credentials
    client_id = os.environ.get('SPOTIFY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)

    # Get the album details from the API
    album = sp.album(album_id)

    # Extract the artist and album name
    artist = album['artists'][0]['name']
    album_name = album['name']

    return artist, album_name

# Read the file containing the list of URLs
file_path = os.path.join(script_directory, 'urls.txt')
with open(file_path, 'r') as file:
    urls = file.read().splitlines()

# Process each URL
for url in urls:
    artist, album_name = parse_spotify_album(url)

    # Create the artist folder inside the Albums folder
    artist_folder = os.path.join(albums_directory, artist)
    os.makedirs(artist_folder, exist_ok=True)

    # Create the album folder inside the artist folder
    album_folder = os.path.join(artist_folder, album_name)
    os.makedirs(album_folder, exist_ok=True)

    # Run a bash command inside the album folder
    os.chdir(album_folder)
    os.system(f"spotdl download '{url}'")  # Added single quotes around the URL

    # Move back to the Albums directory after each iteration
    os.chdir(albums_directory)
