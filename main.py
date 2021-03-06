import os
import time
import json
import dotenv
dotenv.load_dotenv()
import argparse
from datetime import datetime
from util import log
from recently_played import get_recently_played, index_tracks, get_most_recent_timestamp

interval = 30 * 60
limit = 20

def run_scrape():
    while True:
        log.info('Scraping recently played (%s)' % datetime.now())

        output_dir = os.path.join(os.path.dirname(__file__), 'play_history/')

        timestamp = get_most_recent_timestamp(output_dir)
        recently_played = get_recently_played(limit, after=timestamp)
        # index_tracks(recently_played)

        print('Found %d tracks since last scrape' % len(recently_played))
        if len(recently_played) > 0: 
            output_file = os.path.join(output_dir, 'recently_played_%s' % datetime.now())

            with open(output_file, 'w') as f:
                print('Logging to %s' % output_file)
                for track in recently_played:
                    track['_id'] = '%s_%s' % (track['track']['id'], track['played_at'])
                    f.write('%s\n' % json.dumps(track))

        log.info('Sleeping...')
        time.sleep(interval)

def read_json_files(directory, clean):
    if clean:
        print('Deleting files after processing')

    for filename in os.listdir(directory):
        full_path = os.path.join(directory, filename)

        print('Processing %s' % filename)
        with open(full_path) as f:
            tracks = [json.loads(track) for track in f.readlines()]

        index_tracks(tracks)

        if clean:
            os.remove(full_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json')
    parser.add_argument('--clean', action='store_true')

    args = parser.parse_args()

    if args.json:
        print('Reading tracks from JSON files in %s' % args.json)
        read_json_files(args.json, args.clean)
    else:
        print('Starting scrape loop...')
        run_scrape()
