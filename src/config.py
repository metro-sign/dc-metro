from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Network Configuration #
	#########################

	# WIFI Network SSID
	'wifi_ssid': '<wifi name>',

	# WIFI Password
	'wifi_password': '<wifi password>',

	#########################
	# Metro Configuration   #
	#########################

	# API Key for WMATA
	'metro_api_key': '<api key>',

	# Metro Station Codes as a list of strings, number of station codes must match number of train groups
	'metro_station_code': ['D05','D05'],

	# Metro Train Group as list of strings, number of station codes must match number of train groups
	'train_group': ['2','1'],

	#Walking Distance Times, ignore trains arriving in less than this time
	# as list of ints. 
	'walking_time': [0, 0],

	#########################
	# Other Values You      #
	# Probably Shouldn't    #
	# Touch                 #
	#########################
	'metro_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',
	'metro_api_retries': 3,
	'refresh_interval': 5, # 5 seconds is a good middle ground for updates, as the processor takes its sweet ol time

	# Display Settings
	'matrix_width': 64,
	'num_trains': 3,
	'font': bitmap_font.load_font('lib/5x7.bdf'),

	'character_width': 5, #5
	'character_height': 6, #7
	'text_padding': 2, #1
	'text_color': 0xFF7500,

	'loading_destination_text': 'Loading',
	'loading_min_text': '---',
	'loading_line_color': 0xFF00FF, # Something something Purple Line joke

	'heading_text': 'LN DEST   MIN',
	'heading_color': 0xFF0000,

	'train_line_height': 6, #6
	'train_line_width': 4,

	'min_label_characters': 3,
	'destination_max_characters': 8,
}