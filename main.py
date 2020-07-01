 # <iframe src="https://player.twitch.tv/?allowfullscreen&amp;channel=drlupo&amp;origin=https%3A%2F%2Fgtez.org" width="640" height="390" frameborder="0" scrolling="no" allow="autoplay; fullscreen" allowfullscreen=""></iframe>

import logging
import requests
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS


DEBUG = False

default_game = "Dauntless"
default_stream = 'playdauntless'
twitch_api_client_id = 'l9wj3fvnetdz8znlzsi1cav35owwgwk'
default_browser_refresh_rate_seconds = 900 # 15 minutes

# Setup Logging
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)
SCRIPT_FOLDER = os.path.dirname(os.path.realpath(__file__))
HANDLER = logging.FileHandler(os.path.join(SCRIPT_FOLDER, 'app.log'))
# create a logging format
FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

app = Flask(__name__)
app.secret_key = 'cookies-are-fun-bang'
cors = CORS(app)

def get_top_twitch_stream_by_position(position: int, game=default_game) -> str:
	url = "https://api.twitch.tv/kraken/streams/"
	querystring = {"game": game}
	headers = {
		'Accept': "application/vnd.twitchtv.v5+json",
		'Client-ID': twitch_api_client_id,
		'cache-control': "no-cache"
		}
	response = requests.request("GET", url, headers=headers, params=querystring)

	# Filter out mature games to get rid of the button, and prevent the 
	# problems that going to the next stream in the list would cause.
	stream_list = list()
	for stream in response.json()['streams']:
		if stream['channel']['mature']:
			continue
		stream_list.append(stream['channel']['name'])
	try:
		return stream_list[position]
	except IndexError as e:
		logging.error("Error Opening Index {p}".format(p=position))
		if len(stream_list) > 0:
			return stream_list[-1]
		else:
			return default_stream


@app.route("/")
def index():
	idx = int(request.args.get('idx', 0))
	_game = request.args.get('game', default_game)
	_refresh = request.args.get('refresh', default_browser_refresh_rate_seconds)
	streamer = get_top_twitch_stream_by_position(idx, game=_game)
	logging.info(streamer)
	return jsonify({"streamer": streamer, "refresh": _refresh, "index": idx, "game": _game})
	# return render_template('index.html', streamer=streamer, refresh=_refresh)

if __name__ == "__main__":
	if DEBUG:
	    LOGGER.setLevel(logging.DEBUG)
	    HANDLER.setLevel(logging.DEBUG)
	else:
		LOGGER.setLevel(logging.WARN)
		HANDLER.setLevel(logging.WARN)
	app.run(host='0.0.0.0', port=8100, debug=DEBUG)
