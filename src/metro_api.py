import board
from adafruit_matrixportal.network import Network

from config import config
from secrets import secrets

# Keeping a global reference for this
_network = Network(status_neopixel=board.NEOPIXEL)

class MetroApiOnFireException(Exception):
    pass

class MetroApi:
    def fetch_train_predictions(station_code: str, group: str) -> [dict]:
        return MetroApi._fetch_train_predictions(station_code, group, retry_attempt=0)

    def _fetch_train_predictions(station_code: str, group: str, retry_attempt: int) -> [dict]:
        try:
            api_url = config['metro_api_url'] + station_code
            train_data = _network.fetch(api_url, headers={
                'api_key': config['metro_api_key']
            }).json()

            print('Received response from WMATA api...')

            trains = filter(lambda t: t['Group'] == group, train_data['Trains'])

            normalized_results = list(map(MetroApi._normalize_train_response, trains))

            return normalized_results
        except RuntimeError:
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to WMATA API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return MetroApi._fetch_train_predictions(station_code, group, retry_attempt + 1)
            else:
                raise MetroApiOnFireException()
    
    def _normalize_train_response(train: dict) -> dict:
        line = train['Line']
        destination = train['Destination']
        arrival = train['Min']

        if destination == 'No Passenger' or destination == 'NoPssenger' or destination == 'ssenger':
            destination = 'No Psngr'

        return {
            'line_color': MetroApi._get_line_color(line),
            'destination': destination,
            'arrival': arrival
        }
    
    def _get_line_color(line: str) -> int:
        if line == 'RD':
            return 0xFF0000
        elif line == 'OR':
            return 0xFF5500
        elif line == 'YL':
            return 0xFFFF00
        elif line == 'GR':
            return 0x00FF00
        elif line == 'BL':
            return 0x0000FF
        else:
            return 0xAAAAAA
