# This script connects to a Selenium instance (assumed to be running via docker) and uses it
# to login to LastFM and scrape the current list of reccomended tracks. It then uses Pytube to
# download the MP3s using pytube, create an M3U playlist file, and put them in a folder

import os
import re
import datetime
from dotenv import load_dotenv
from pytube import YouTube
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# Load environment variables from .env file
load_dotenv()

def sanitize_filename(name):
    unsafe_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in unsafe_characters:
        name = name.replace(char, '')
    return name

def login_to_website():
    # Define the Chrome options
    chrome_options = Options()
    chrome_options.set_capability("browserName", "chrome")

    driver = None
    tracks = []  # List to store the track information

    try:
        # Setting up Remote Webdriver to connect to the Selenium standalone Chrome Docker container
        driver = webdriver.Remote(
            command_executor='http://localhost:4444/wd/hub',
            options=chrome_options)

        # Opening the website
        driver.get("https://www.last.fm/login")

        username_field = driver.find_element(By.NAME, 'username_or_email')
        username_field.send_keys(os.environ.get('LASTFM_USERNAME'))

        password_field = driver.find_element(By.NAME, 'password')
        password_field.send_keys(os.environ.get('LASTFM_PASSWORD'))

        login_button = driver.find_element(By.NAME, 'submit')
        login_button.click()

        WebDriverWait(driver, 10).until(EC.url_changes("https://www.last.fm/login"))
        driver.get("https://www.last.fm/home/tracks")

        recs_feed_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".recs-feed-item")))

        for item in recs_feed_items:
            try:
                recs_feed_playlink = item.find_element(By.CSS_SELECTOR, ".recs-feed-playlink").get_attribute("href")
            except NoSuchElementException:
                print("Playlink selector missing")
                continue  # Skip this item if the playlink is missing

            track_name_dirty = item.find_element(By.CSS_SELECTOR, ".recs-feed-title a").text
            # Here we clean up the track_name by removing the duration using regex
            track_name = re.sub(r'\s\(\d+:\d+\)$', '', track_name_dirty)

            artist_name = item.find_element(By.CSS_SELECTOR, ".recs-feed-description a").text

            print(f"Playlink: {recs_feed_playlink}, Track Name: {track_name}, Artist Name: {artist_name}")

            # Add the track information to the list
            tracks.append((recs_feed_playlink, track_name, artist_name))

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if driver is not None:
            driver.quit()

    # After quitting the driver, download each track
    parent_dir = 'LastFM Recommendations'
    if not os.path.exists(parent_dir):
        os.makedirs(parent_dir)

    dir_name = 'LFM - ' + datetime.datetime.now().strftime('%m-%d-%y')
    dir_path = os.path.join(parent_dir, dir_name)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    playlist = []  # List to store the filenames for the M3U playlist

    for playlink, track_name, artist_name in tracks:
        try:
            youtube = YouTube(playlink)
            stream = youtube.streams.get_audio_only()
            sanitized_track_name = sanitize_filename(track_name)
            sanitized_artist_name = sanitize_filename(artist_name)
            filename = f"{sanitized_artist_name} - {sanitized_track_name}.mp3"
            output_file = stream.download(output_path=dir_path, filename=filename)  # Downloads the video

            # Add the filename to the playlist
            playlist.append(output_file)

        except Exception as e:
            print(f"An error occurred while downloading {playlink}: {e}")

    # Create the M3U playlist
    with open(os.path.join(dir_path, f"{dir_name}.m3u"), 'w') as f:
        for filename in playlist:
            f.write(os.path.basename(filename) + '\n')

if __name__ == "__main__":
    login_to_website()
