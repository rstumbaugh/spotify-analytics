#! /bin/bash

root=~/Development/repos/spotify-elastic
play_history_dir=play_history

venv_dir=~/Development/envs/spotify-analytics

cd $root

echo [update_local_elastic] Cleaning output dir
rm -rf $play_history_dir/*

echo [update_local_elastic] Getting scrape data from ec2
scripts/get_latest_scrapes.sh

echo [update_local_elastic] Indexing latest scrapes
source $venv_dir/bin/activate
python main.py --json $play_history_dir --clean

echo [update_local_elastic] Done