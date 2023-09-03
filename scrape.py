import os
import requests
from bs4 import BeautifulSoup
import json
import tkinter as tk
from tkinter import messagebox
import pyperclip

# Check if the environment variables are set, otherwise prompt the user to enter them
qobuz_app_id = os.getenv('QOBUZ_APP_ID')
qobuz_auth_token = os.getenv('QOBUZ_AUTH_TOKEN')

if not qobuz_app_id:
    qobuz_app_id = input("QOBUZ_APP_ID environment variable is not set. Please enter your Qobuz App ID: ")

if not qobuz_auth_token:
    qobuz_auth_token = input("QOBUZ_AUTH_TOKEN environment variable is not set. Please enter your Qobuz Auth Token: ")

# TODO: Add description
# TODO: Add error handling for invalid credentials
# TODO: Add error handling for invalid URL

# Function to process and write IDs to a file and copy to clipboard
def process_and_write_ids(ids, id_type):
    urls = []  # List to store URLs
    file_name = f"{id_type}s.txt"
    with open(file_name, "w") as file:
        for id in ids:
            url = f"https://play.qobuz.com/{id_type}/" + str(id)
            file.write(url + "\n")
            urls.append(url)  # Append URL to the list
            print(url)
    urls_text = "\n".join(urls)  # Join URLs into a single string
    pyperclip.copy(urls_text)  # Copy to clipboard

# Function to handle button clicks
def on_choice_button_click(choice):
    if choice == 1:
        params = {'type': 'artists'}
    elif choice == 2:
        params = {'type': 'albums'}
    elif choice == 3:
        params = {'type': 'tracks'}
    else:
        messagebox.showerror("Error", "Invalid choice.")
        return

    headers = {
        'X-App-Id': qobuz_app_id,
        'X-User-Auth-Token': qobuz_auth_token
    }

    response = requests.get('https://www.qobuz.com/api.json/0.2/favorite/getUserFavoriteIds?limit=5000', params=params, headers=headers)

    if response.status_code != 200:
        messagebox.showerror("Error", f"Unable to fetch data. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'lxml')
    json_data = soup.find('p').text
    data = json.loads(json_data)

    # Process and write IDs based on the user's choice
    if choice == 1:
        process_and_write_ids(data['artists'], 'artist')
    elif choice == 2:
        process_and_write_ids(data['albums'], 'album')
    elif choice == 3:
        process_and_write_ids(data['tracks'], 'track')

# Create the main application window
root = tk.Tk()
root.title("Qobuz Data Fetcher")

# Create a label to prompt the user
prompt_label = tk.Label(root, text="Please select one of the following options:")
prompt_label.pack()

# Create and pack choice buttons
artist_button = tk.Button(root, text="Artists", command=lambda: on_choice_button_click(1))
artist_button.pack()

album_button = tk.Button(root, text="Albums", command=lambda: on_choice_button_click(2))
album_button.pack()

track_button = tk.Button(root, text="Tracks", command=lambda: on_choice_button_click(3))
track_button.pack()

# Start the GUI main loop
root.mainloop()
