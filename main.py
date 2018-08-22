import os
import time
import json
import dotenv
dotenv.load_dotenv()
from datetime import datetime
from util import log
from recently_played import get_recently_played, index_tracks

interval = 30 * 60
limit = 20

if __name__ == '__main__':
    while True:
        log.info('Scraping recently played (%s)' % datetime.now())

        recently_played = get_recently_played(limit)
        # index_tracks(recently_played)
        
        output_dir = os.path.join(os.path.dirname(__file__), 'play_history/recently_played_%s' % datetime.now())
        with open(output_dir, 'w') as f:
            print('Logging to %s' % output_dir)
            for track in recently_played:
                track['_id'] = '%s_%s' % (track['track']['id'], track['played_at'])
                f.write('%s\n' % json.dumps(track))

        log.info('Sleeping...')
        time.sleep(interval)