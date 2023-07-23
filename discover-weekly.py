# This script downloads your Spotify Discover Weekly playlist using spotdl, creates an M3U playlist file, and then moves everything into a folder

import os
from dotenv import load_dotenv
import subprocess
import smtplib
from datetime import datetime
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

def create_m3u_playlist(directory):
    # Get the list of MP3 files in the directory
    mp3_files = [file for file in os.listdir(directory) if file.endswith(".mp3")]

    # Create the M3U playlist file
    today = datetime.now().strftime("%m-%d-%Y")
    playlist_name = f"DW - {today}.m3u"
    playlist_path = os.path.join(directory, playlist_name)
    with open(playlist_path, "w") as playlist_file:
        # Write the header
        playlist_file.write("#EXTM3U\n")

        # Write each MP3 file path as a playlist entry
        for mp3_file in mp3_files:
            mp3_path = os.path.join(mp3_file)
            playlist_file.write(f"#EXTINF:0,{mp3_file}\n")
            playlist_file.write(f"{mp3_path}\n")

    print(f"M3U playlist created: {playlist_path}")

def create_folder_with_current_date(subfolder):
    current_date = datetime.now().strftime("%m-%d-%Y")
    folder_path = os.path.join(os.getcwd(), subfolder, current_date)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

def execute_bash_command(command, folder_path):
    try:
        # Change directory to the created folder
        os.chdir(folder_path)

        # Execute the bash command
        # process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        # stdout, stderr = process.communicate()
        # print(process.stdout)
        print(process.stderr)

        if process.returncode == 0:
            send_email(f"Discover Weekly List Updated", f"A new discover weekly playlist has been downloaded to ${folder_path}")
            print("Command executed successfully.")
        else:
            error_message = f"Command execution error:\n{process.stderr}"
            print(error_message)  # Print the error message on the console
            send_email(f"${script_name} - Command Execution Error", error_message)

    except Exception as e:
        print(e)
        send_email(f"${script_name} - Command Execution Error", str(e))

def send_email(subject, message):
    # Gmail SMTP configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = os.environ.get('EMAIL_SENDER')
    sender_app_password = os.environ.get('EMAIL_APP_PASSWORD')
    recipient_email = os.environ.get('EMAIL_RECIPIENT')

    # Email content
    email_subject = subject
    email_body = message

    # Create email message
    msg = MIMEText(email_body)
    msg['Subject'] = email_subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_app_password)
            server.send_message(msg)
        print("Email sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {str(e)}")

script_name = 'Discover Weekly'
subfolder = 'Discover Weekly'
command_to_execute = ['spotdl', 'download', 'https://open.spotify.com/playlist/37i9dQZEVXcSGDho0HZ8IY?si=f8a39d9e692f4610']
folder_path = create_folder_with_current_date(subfolder)
execute_bash_command(command_to_execute, folder_path)
create_m3u_playlist(folder_path)

