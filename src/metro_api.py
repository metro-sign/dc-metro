import board
from adafruit_matrixportal.network import Network
import time

from config import config
from secrets import secrets

# Keeping a global reference for this
_network = Network(status_neopixel=board.NEOPIXEL)

class MetroApiOnFireException(Exception):
    pass

class MetroApi:
    def fetch_train_predictions(station_codes, groups, walks={}) -> [dict]:
        return MetroApi._fetch_train_predictions(station_codes, groups, walks, retry_attempt=0)

    def _fetch_train_predictions(station_codes, groups, walks, retry_attempt: int) -> [dict]:
        try:
            start = time.time()
            print('Fetching...')
            api_url = config['metro_api_url'] + ','.join(set(station_codes))
            train_data = _network.fetch(api_url, headers={
                'api_key': config['metro_api_key']
            }).json()
            print('Received response from WMATA api...')
            TIME_BUFFER = round((time.time() - start)/60) + 1
         
            trains = [MetroApi._normalize_train_response(t, TIME_BUFFER) for t in train_data['Trains']]
            print(trains)
            print('Filtering Results')
            if walks == {}:
                trains = list(filter(lambda t: (t['loc'], t['group']) in groups, trains))
            else:
                trains = list(filter(lambda t: ((t['loc'], t['group']) in groups and MetroApi.arrival_map(t['arrival'])-walks[t['loc']] >= 0), trains))
            
            if len(groups) > 1:
                trains = sorted(trains, key=lambda t: MetroApi.arrival_map(t['arrival']))
            print(trains)
            print('Time to Update: ' + str(time.time() - start))
            return trains

        except RuntimeError:
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to WMATA API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return MetroApi._fetch_train_predictions(station_codes, groups, walks, retry_attempt + 1)
            else:
                raise MetroApiOnFireException()

    def arrival_map(arr):
        if arr == 'BRD' or arr == 'ARR':
            return 0
        elif not arr.isdigit():
            return 100
        else:
            return int(arr)

    def _normalize_train_response(train: dict, buff:int) -> dict:
        line = train['Line']
        destination = train['Destination']
        group = train['Group']
        loc = train['LocationCode']
        arrival = train['Min']

        #Adjust for time to wait for the REST API
        if arrival.isdigit():
            arrival = int(arrival) - buff
            if arrival <= 0: 
                arrival = 'ARR'
            else:
                arrival = str(int(arrival))

        if destination == 'No Passenger' or destination == 'NoPssenger' or destination == 'ssenger':
            destination = 'No Psngr'

        return {
            'line_color': MetroApi._get_line_color(line),
            'destination': destination,
            'arrival': arrival,
            'group': group,
            'loc': loc
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
