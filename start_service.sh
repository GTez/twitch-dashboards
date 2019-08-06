#!/usr/bin/env bash
DIR="/opt/gtez/twitch-dashboards" 

if ! [ -d "$DIR/venv" ]; then
	virtualenv -p python3 $DIR/venv
	source $DIR/venv/bin/activate
	cd $DIR
	pip3 install -r requirements.txt
fi

cd $DIR
source $DIR/venv/bin/activate
/usr/bin/screen -S twitch-dashboard -d -m $DIR/venv/bin/gunicorn main:app -b 0.0.0.0:8100 -w 2

