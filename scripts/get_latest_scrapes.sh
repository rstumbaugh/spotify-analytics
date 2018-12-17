#! /bin/bash

app_name=spotify-elastic
root=~/Development/repos/spotify-elastic
output_dir=play_history
ssh_key=~/Development/keys/aws/rstum.pem
version=`cat $root/__version__`

clean="y"

user=ec2-user
host=ec2-18-234-115-133.compute-1.amazonaws.com
scrapes=/home/$user/$app_name'_'$version/play_history

cd $root

if [ $# -eq 0 ]; then
    echo [get_latest_scrapes] Deleting old scrapes on completion
elif [ $1 = "--no-clean" ]; then
    clean="n"
    echo [get_latest_scrapes] Not deleting old scrapes on completion
fi

mkdir $output_dir
rm -rf $output_dir/*

echo [get_latest_scrapes] Outputting scrape data to from $scrapes to $output_dir

scp -i $ssh_key $user@$host:$scrapes/* $output_dir/

echo [get_latest_scrapes] Got latest scrapes

if [ $clean = "y" ]; then
    ssh -i $ssh_key $user@$host rm -f $scrapes/*
    echo [get_latest_scrapes] Cleaned old scrapes
fi

echo [get_latest_scrapes] Done