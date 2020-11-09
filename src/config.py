from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Network Configuration #
	#########################

	# WIFI Network SSID
	'wifi_ssid': '<Your 2.4ghz WiFi SSID>',

	# WIFI Password
	'wifi_password': '<Your WiFi Password>',

	#########################
	# Metro Configuration   #
	#########################

	# Metro Station Code
	'metro_station_code': 'D02',

	# Metro Train Group
	'train_group': '2',

	# API Key for WMATA
	'metro_api_key': '<Your WMATA API Key>',

	#########################
	# Other Values You      #
	# Probably Shouldn't    #
	# Touch                 #
	#########################
	'metro_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',
	'metro_api_retries': 3,
	'refresh_interval': 5,

	# Display Settings
	'matrix_width': 64,
	'num_trains': 3,
	'font': bitmap_font.load_font('lib/5x7.bdf'),

	'character_width': 5,
	'character_height': 7,
	'text_padding': 1,
	'text_color': 0xFF7500,

	'loading_destination_text': 'Loading',
	'loading_min_text': '---',
	'loading_line_color': 0xFF00FF, # Something something Purple Line joke

	'heading_text': 'LN DEST   MIN',
	'heading_color': 0xFF0000,

	'train_line_height': 6,
	'train_line_width': 2,

	'min_label_characters': 3,
	'destination_max_characters': 8,

	# Refresh Settings
	'refresh_interval': 10, # 10 seconds is a good middle ground for updates
}