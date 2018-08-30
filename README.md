# spotify-analytics
Python script to index my Spotify listening data to Elasticsearch

Currently running on an AWS EC2 instance scraping 20 recent tracks every 30 minutes. 
Listening history is currently being logged to JSON files which I pull and index into my local Elasticsearch instance. Kibana is also being used for visualization dashboards.

Future plans include a recommendation engine, creating Spotify playlists, and support for multiple users.
