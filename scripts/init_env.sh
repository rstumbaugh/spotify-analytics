#! /bin/bash

venv_dir=$1
app_dir=$2

cd $app_dir

echo [init_env] Creating venv in $venv_dir
rm -rf $venv_dir
python3 -m venv $venv_dir
source $venv_dir/bin/activate


echo [init_env] Installing dependencies from $app_dir/requirements.txt
pip install -r $app_dir/requirements.txt

echo [init_env] Setting environment variables
source $app_dir/.env