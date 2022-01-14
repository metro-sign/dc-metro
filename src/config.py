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
	'source_api': 'WMATA', # WMATA or MetroHero.

	# WMATA / MetroHero API Key
	'wmata_api_key': '',
	'metro_hero_api_key': '',

	# Metro Station Code
	'metro_station_codes': ['E03','C02'],

	# Metro Train Group
	'train_groups': ['2','2'],

	#Walking Distance Times, ignore trains arriving in less than this time
	# [2, 12]
	'walking_times': [8, 8],

	# WMATA API
	'wmata_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',

	# # MetroHero API
	'metro_hero_api_url': 'https://dcmetrohero.com/api/v1/metrorail/stations/[stationCode]/trains?includeScheduledPredictions=True',

	'metro_api_retries': 3,
	'refresh_interval': 5, # 5 seconds is a good middle ground for updates, as the processor takes its sweet ol time

        # Full names mapped to abbreviations for MetroHero
        'station_mapping': {
            'Branch Avenue': 'Brnch Av',
            'Huntington': 'Hntingtn',
            'Vienna/Fairfax-GMU': 'Vienna',
            'Franconia-Springfield': 'Frnconia',
            'New Carrollton': 'NewCrltn',
            'Greenbelt': 'Grnbelt',
            'Huntington': 'Hntingtn',
            'Largo Town Center': 'Largo',
            'Twinbrook': 'Twinbrk',
            'Wiehle-Reston East': 'Wiehle',
            'No Passenger': 'No Psngr',
            'NoPssenger': 'No Psngr',
            'ssenger': 'No Psngr'

        },

    #############################
    # Off Hours Configuration   #
    #############################

    # adafruit io settings, necessary for determining current time to sleep
    # An account is free to set up, instructions below
    # https://learn.adafruit.com/adafruit-magtag/getting-the-date-time
    'aio_username': '',
    'aio_key': '',

    # Time of day to turn board on and off - must be 24 hour "HH:MM"
    'display_on_time': "07:00",
    'display_off_time': "22:00",


    #########################
    # Display Configuration #
    #########################
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
