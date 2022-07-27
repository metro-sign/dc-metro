from config import config

# This file is required by the Matrix Portal library to properly
# initialize the WiFi chip on the board.
#
# Why isn't aren't the SSID and password just parameters for the
# connect function? The world may never know :(
secrets = {
    'ssid': config['wifi_ssid'],
    'password': config['wifi_password'],
    'aio_username': config.get('aio_username'),
    'aio_key': config.get('aio_key'),
    'timezone': 'America/New_York',
}
