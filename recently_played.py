import json
from datetime import datetime
from util import log, api, elasticsearch

def format_artist(artist):
    return artist['id']

def format_album(album):
    return {
        'name': album['name'],
        'uri': album['uri'],
        'id': album['id']
    }

def format_track(track):
    album = track['album']
    artists = track['artists']

    return {
        'album': format_album(album),
        'artists': [format_artist(a) for a in artists],
        'name': track['name'],
        'uri': track['uri'],
        'id': track['id']
    }

def format_item(item):
    return {
        'track': format_track(item['track']),
        'played_at': item['played_at']
    }

def get_recently_played(limit):
    log.info('Getting recently played tracks...')
    endpoint = '/me/player/recently-played'
    query_params = {
        'limit': limit
    }

    response = api.get(endpoint, query_params)

    if response.status_code not in [200, 201]:
        log.info('Error getting recently played')
        log.info(response.text)
        return []

    items = response.json()['items']
    return [format_item(item) for item in items]

def index_tracks(tracks):
    indexed = 0
    for track in tracks:
        track_id = track['track']['id']
        timestamp = track['played_at']

        if '_id' in track:
            doc_id = track['_id']
            del track['_id']
        else:
            doc_id = '%s_%s' % (track_id, timestamp)

        if not elasticsearch.track_exists(doc_id):
            elasticsearch.index_track(track, doc_id)
            indexed += 1

    log.info('Indexed %d of %d tracks' % (indexed, len(tracks)))
