import requests
from bs4 import BeautifulSoup
import json

#TODO, add description
#TODO, get app-id and user auth token from login
#TODO, add user input for x-app-id and x-user-auth-token/username and password
#TODO, add error handling for invalid credentials
#TODO, add error handling for invalid url
#TODO, add list of favorite albums
#TODO, add list of favorite tracks

with open('headers.json', 'r') as f:
    headers = json.load(f)

params = {
    'type': 'artists'
}

response = requests.get('https://www.qobuz.com/api.json/0.2/favorite/getUserFavorites', params=params, headers=headers)
soup = BeautifulSoup(response.text, 'lxml')
json_data = soup.find('p').text
data = json.loads(json_data)

ids = ["https://play.qobuz.com/artist/"+ str(item['id']) for item in data['artists']['items']]
file = open("artists.txt", "w")

for id in ids:
    file.write(id + "\n")
    print(id)

file.close()