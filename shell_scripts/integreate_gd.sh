#!/bin/bash

PROJECT_DIR="$(dirname "$0")"
source $PROJECT_DIR/../.venv/bin/activate
#write out current crontab
crontab -l > mycron
#echo new cron into cron file
echo "0 1 * * * python $PROJECT_DIR/../python_scripts/read_drive.py" >> mycron
#install new cron file
crontab mycron
rm mycron