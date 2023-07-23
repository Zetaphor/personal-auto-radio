# This script processes the starred tracks from a Navidrome database that are in the
# Discover Weekly and LastFM playlists that were created by the other scripts. It moves
# any starred tracks from those playlists to a Reccomendations folder and then removes
# the playlist and remaining unstarred MP3s

import sqlite3
import shutil
import os

# Connect to the SQLite database
conn = sqlite3.connect('/srv/docker/navidrome/data/navidrome.db')

# Create a cursor object
cur = conn.cursor()

# Construct and execute the query
query = """
SELECT mf.path AS track_path, pl.path AS playlist_path
FROM annotation an
JOIN media_file mf ON an.item_id = mf.id
JOIN playlist_tracks pt ON mf.id = pt.media_file_id
JOIN playlist pl ON pt.playlist_id = pl.id
WHERE an.starred = 1 AND (pl.name LIKE 'DW -%' OR pl.name LIKE 'LFM -%')
"""

cur.execute(query)
results = cur.fetchall()

# Close the connection
conn.close()

# Create target directory if it doesn't exist
target_dir = "/srv/Spotify/Liked Songs/Recommendations"
os.makedirs(target_dir, exist_ok=True)

# Set of unique playlist paths
playlist_paths = set()

# Copy the files
for row in results:
    track_path, playlist_path = row
    playlist_paths.add(playlist_path)
    if os.path.isfile(track_path):
        shutil.copy2(track_path, target_dir)
        os.remove(track_path)  # remove the original file
    else:
        print(f"File does not exist: {track_path}")

# Remove the playlist files
for playlist_path in playlist_paths:
    if os.path.isfile(playlist_path):
        os.remove(playlist_path)
    else:
        print(f"Playlist file does not exist: {playlist_path}")
