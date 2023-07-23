# This script downloads a Youtube Playlist to MP3's using pytube

import os
from pytube import Playlist
from pydub import AudioSegment

# YouTube playlist URL
playlist_url = "https://www.youtube.com/playlist?list=PLBsYxkIK0syHwPBaYQqDWkaTx7KklPovT"

# Create a directory to store the downloaded videos
output_dir = "downloaded_videos"
os.makedirs(output_dir, exist_ok=True)

# Download the videos using pytube
playlist = Playlist(playlist_url)

for video in playlist.videos:
    title = video.title
    stream = video.streams.get_audio_only()
    stream.download(output_path=output_dir)

# Convert the downloaded videos to MP3
for filename in os.listdir(output_dir):
    if filename.endswith(".mp4"):
        mp4_file = os.path.join(output_dir, filename)
        mp3_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".mp3")
        audio = AudioSegment.from_file(mp4_file, "mp4")
        audio.export(mp3_file, format="mp3")
        os.remove(mp4_file)
