from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ':' + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_album(token, album, artist):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #can make query more specific with artist name
    query = f"?q={album}&type=album&{artist}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)['albums']['items']

    if len(json_result) == 0:
        print("Nothing found")
        return None
    
    return (json_result[0]['id'], json_result[0]['name'])

def get_album_tracks(token, id):
    url = f"https://api.spotify.com/v1/albums/{id}/tracks"
    headers = get_auth_header(token)
    query = f"?limit=30&market=US"

    result = get(url + query, headers=headers)
    json_result = json.loads(result.content)

    return json_result['items']

def get_artist_id(token,artist):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    #can make query more specific with artist name
    query = f"?q={artist}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)

    if len(json_result) == 0:
        print("Nothing found")
        return None
    
    return json_result['artists']['items'][0]['id']



token = get_token()
# album = search_for_album(token, "gnx", "kendrick lamar")
# print(get_album_tracks(token, album[0]))

print(get_artist_id(token, 'Various artists'))





