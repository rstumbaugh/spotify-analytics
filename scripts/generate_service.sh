#! /bin/bash

python_path=$1
main_py_path=$2
service_output=$3
log_file=$4

echo [generate_service] Generating systemd service to $service_output

# generate systemd service file
echo \
"[Unit]
Description=Spotify Analytics
After=systemd-user-sessions.service

[Service]
Type=simple
ExecStart=$python_path $main_py_path" > $service_output