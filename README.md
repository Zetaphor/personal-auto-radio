# Personal Auto Radio

## Project Overview

This project contains a collection of Python scripts that automate the download of MP3s from Spotify, YouTube, and LastFM.

## Purpose

My use case is to create a way of getting new recommendations for use with my self-hosted radio station and music catalog, using [Azuracast](https://www.azuracast.com/) and [Navidrome](https://www.navidrome.org/).

There are two scripts I run every Monday, `discover-weekly.py` and `lastfm-recommendations.py` which gather my current recommendations from each service, and create a playlist file for the collection from that week.

I then review that weeks content by listening through each weekly playlist in Navidrome where I decide what tracks I will keep as part of my permanent library by using the "star" feature (the heart button).

Then at the end of each week I run the `process-starred.py` script, which reads the generated playlists, moves any starred tracks into my permanent library, and deletes the remaining MP3's and the generated playlists.

These tracks are then automatically added into the rotation on my Azuracast radio station, which is cycling through my entire library.

## Scripts

### Manual Scripts

These manual scripts were used to bootstrap my library. These allowed me to import my existing Youtube and Spotify playlists, as well as to grab artists/albums from Spotify in bulk.

#### `youtube-playlist.py`

This script downloads a YouTube playlist as MP3 files using the `pytube` library.

#### `spotify-downloader.py`

This script uses the `spotipy` library to download music from Spotify. It loads a text file of Spotify share URLs (albums or playlists) and downloads them as MP3 files. The script automatically creates a folder for each artist and then creates subfolders for each album. The script expects the URL's to be stored in a file called `urls.txt`. Note this script requires a `client_id` and `client_secret` in order to use the Spotify API. These are used to scrape the artist and album details from the URL in order to create the folders. These values are defined in the environment variables file described below.

### Automated Scripts

#### `discover-weekly.py`

This script uses `spotipy` to download the user's Spotify "Discover Weekly" playlist. It converts the downloaded songs into MP3 format. After downloading, it creates an M3U playlist file. The script then moves all the MP3 files and the M3U playlist file into a folder named "DW - `<date>`", where `<date>` is the current date. Upon success/failure the script will send an email using the GMail SMTP server. See the "Environment Variables" section below for configuration details.

#### `lastfm-recommendations.py`

This script connects to a Selenium instance running via Docker to log in to LastFM and scrape the current list of recommended tracks. It uses `pytube` to download these recommended tracks in MP3 format. After downloading, it creates an M3U playlist file. The script then moves all the MP3 files and the M3U playlist file into a folder named "LFM - `<date>`", where `<date>` is the current date. The authentication details for the LastFM user are defined in the environment variables file described below.

#### `process-starred.py`

This script processes the starred tracks from a Navidrome database. It specifically targets the "DW - \<date\>" (Discover Weekly) and "LFM - \<date\>" (LastFM) playlists created by the `discover-weekly.py` and `lastfm-recommendations.py` scripts. It moves any starred tracks from these playlists to a "Recommendations" folder. After moving the starred tracks, it removes the M3U playlist file and the remaining unstarred MP3s. This way, only the MP3s that have been starred in Navidrome are kept in the "Recommendations" folder.

## Setup

### Install Requirements

Install the required Python packages by running `pip install -r requirements.txt`.

### Environment Variables

These scripts assume the presence of a `.env` file which contains the following variables:

```
EMAIL_SENDER=
EMAIL_APP_PASSWORD=
EMAIL_RECIPIENT=
LASTFM_USERNAME=
LASTFM_PASSWORD=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

Populate this file with the required values as needed by the scripts you intend to use.

You can obtain a Spotify `client_id` and `client_secret` by creating an app on the [Developer Dashboard](https://developer.spotify.com/dashboard).

You can obtain an `app_password` for GMail by following [the instructions here](https://support.google.com/accounts/answer/185833?hl=en). This assumes you have 2-Factor authentication enabled for your Google account. If you don't have that enabled, go fix that immediately.

## Usage

Each script can be run from the command line using the `python <script-name>.py` command. For example, to run the `youtube-playlist.py` script, you would use the command `python youtube-playlist.py`.

#### Manual Scripts

To use the `spotify-downloader.py` script simply populate the `urls.txt` file with the Spotify share URLs for the albums or playlists you want to download, one item per line.

For the `discover-weekly.py` and `lastfm-recommendations.py` scripts, schedule a cron job to run them every Monday. For the `lastfm-recommendations.py` script, you will need to have a Selenium instance running in Docker. You can use the `docker-selenium.sh` script to set this up. It's reccomended to start with a cron job before the LastFM script runs, and then stop the container with another cron job after it completes. It's not advised to leave this container running outside of the window where the scripts are running if you're using this on an internet accessible host.

# Created By ChatGPT

Every script in this repo was originally written by a combination of GPT-3.5 and GPT-4 combined with the Code Interpreter feature. The `process-starred` script in particular was written by uploading the sqlite database from Navidrome into the GPT-4 Code Interpreter and telling it to find where starred tracks are stored. From there I instructed it to filter by the specific playlist naming I use, move the files, and remove the rest.

This entire project was built over a collective period of maybe 4 hours of prompting, testing/validating output, and then further iterating on the requirements with additional prompting.

Even the initial draft of this README was written by uploading the scripts to GPT-4 with Code Interpreter (you can give it a zip file and tell it to look in there), giving it a basic description of the project, and instructing it to further analyze the files and create the skeleton that became this final document.

If you're not using these tools already to bootstrap and empower your development cycles, you're really missing out. I probably wouldn't have even bothered starting this project purely based on the time commitement it would have taken for me to research and iterate all of the different components. Instead I was able to go from initial idea to final product in a matter of hours.

AI is not going to replace developers, developers who use AI are going to replace developers.

# License

This software is licensed under the WTFPL. Enjoy!
