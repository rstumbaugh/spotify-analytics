import time
import dotenv
dotenv.load_dotenv()
from datetime import datetime
from recently_played import get_recently_played, index_tracks

interval = 30 * 60

if __name__ == '__main__':

    while True:
        print('Scraping recently played (%s)' % datetime.now())

        #recently_played = get_recently_played()
        #index_tracks(recently_played)

        print('Sleeping...')
        time.sleep(interval)