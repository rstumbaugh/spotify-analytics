#! /bin/bash

service_name=$1
service_path=$2

echo [install_service] Stopping existing service
sudo systemctl stop $service_name

echo [install_service] Installing $service_name
sudo mv $service_path/$service_name /etc/systemd/system/
sudo systemctl daemon-reload

echo [install_service] Starting service
sudo systemctl start $service_name