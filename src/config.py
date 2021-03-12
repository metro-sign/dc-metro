from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Network Configuration #
	#########################

	# WIFI Network SSID
	'wifi_ssid': '',

	# WIFI Password
	'wifi_password': '',

	#########################
	# Metro Configuration   #
	#########################
	# WMATA API KEY
	'source_api': 'WMATA', # WMATA or MetroHero. MetroHero currently doesn't work, so do not use.
	'metro_api_key1': '',

	# Metro Station Code
	#Cap South, Navy Yard
	'metro_station_code': ['D05','F05'],

	# Metro Train Group
	'train_group': ['2','1'],

	#Walking Distance Times, ignore trains arriving in less than this time
	# [2, 12]
	'walking_time': [2, 12],

	#########################
	# Other Values You      #
	# Probably Shouldn't    #
	# Touch                 #
	#########################
		# WMATA API
	'metro_api_url1': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',

	# # MetroHero API - Not Current Working with the code. No need to fill or use
	'metro_api_url2': 'https://dcmetrohero.com/api/v1/metrorail/stations/[stationCode]/trains',
	'metro_api_key2': '',
	
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