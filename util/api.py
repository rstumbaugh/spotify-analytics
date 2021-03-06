# Spotify API utils
import os
import json
import base64
import requests
from urllib.parse import urlencode
from util import log

client_id = os.environ['SPOTIFY_CLIENT_ID']
client_secret = os.environ['SPOTIFY_CLIENT_SECRET']

# probably want to move this to a DB at some point
# would be much better to extend for multiple users if stored in a DB
file_path = os.path.dirname(__file__)
access_token_path = os.path.join(file_path, '../priv/access_token')
refresh_token_path = os.path.join(file_path, '../priv/refresh_token')
with open(access_token_path) as f:
    global access_token
    access_token = f.readline()

with open(refresh_token_path) as f:
    global refresh_token
    refresh_token = f.readline()

def get(endpoint, url_params=None, access_token=access_token, refresh_token=refresh_token):
    url = 'https://api.spotify.com/v1%s' % endpoint
    if access_token:
        auth_header = 'Bearer {}'.format(access_token)
    else:
        auth_header = get_auth_header()

    header = {
        'Authorization': auth_header
    }

    if url_params:
        url += '?%s' % urlencode(url_params)

    r = requests.get(url, headers=header)
    if r.status_code == 401 and access_token is not None:
        log.info('Refreshing access token')
        new_token = refresh_access_token(refresh_token)
        if new_token is None:
            log.info('Error refreshing access token')
            return None

        update_access_token(new_token)

        header = { 'Authorization': 'Bearer {}'.format(new_token) }
        r = requests.get(url, headers=header)
        log.info('Access token refreshed successfully')

    elif r.status_code == 429:
        wait = int(r.headers['retry-after'])
        log.info('Rate limit exceeded, waiting %d seconds' % wait)
        return get(endpoint, url_params, access_token, refresh_token)

    return r

def get_auth_header():
    auth_str = '{}:{}'.format(client_id, client_secret)
    b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()
    return 'Basic {}'.format(b64_auth_str)

def refresh_access_token(refresh_token):
    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Authorization': get_auth_header()
    }

    r = requests.post(url, data=body, headers=headers)
    if r.status_code is not 200:
        return None
    else:
        json = r.json()
        return json['access_token']

def update_access_token(new_token):
    global access_token
    with open(access_token_path, 'w') as f:
        f.write(new_token)
    access_token = new_token
