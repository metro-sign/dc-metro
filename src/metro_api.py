import board
import time

from config import config
from secrets import secrets

class MetroApiOnFireException(Exception):
    pass

class MetroApi:
    def fetch_train_predictions(wifi, station_codes, groups, walks={}) -> [dict]:
        return MetroApi._fetch_train_predictions(wifi, station_codes, groups, walks, retry_attempt=0)

    def _fetch_train_predictions(wifi, station_codes, groups, walks, retry_attempt: int) -> [dict]:
        try:
            print('Fetching...')
            start = time.time()

            if config['source_api'] == 'WMATA':
                # WMATA Method
                api_url = config['metro_api_url1'] + ','.join(set(station_codes))
                response = wifi.get(api_url, headers={'api_key': config['metro_api_key1']}, timeout=30).json()
                trains = list(filter(lambda t: (t['LocationCode'], t['Group']) in groups, response['Trains']))
            else:
                #Metro Hero Method
                trains = []
                for station in set(station_codes): # select trains in desired direction
                    api_url = config['metro_api_url2'].replace('[stationCode]', station)
                    response = wifi.get(api_url, headers={'apiKey': config['metro_api_key2']}, data={'includeScheduledPredictions':True}, timeout = 60).json()
                    trains.extend(list(filter(lambda t: (station, t['Group']) in groups, response)))

            print('Received response from ' + config['source_api'] + ' api...')
            TIME_BUFFER = round((time.time() - start)/60) + 1
            trains = [MetroApi._normalize_train_response(t, TIME_BUFFER) for t in trains]

            if walks != {}:
                trains = list(filter(lambda t: MetroApi.arrival_map(t['arrival'])-walks[t['loc']] >= 0, trains))

            if len(groups) > 1:
                trains = sorted(trains, key=lambda t: MetroApi.arrival_map(t['arrival']))

            print(trains)
            print('Time to Update: ' + str(time.time() - start))
            return trains

        except:
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return MetroApi._fetch_train_predictions(wifi, station_codes, groups, walks, retry_attempt + 1)
            else:
                raise MetroApiOnFireException()

    def arrival_map(arr):
        if arr == 'BRD':
            return 0
        elif arr == 'ARR':
            return 1
        elif not arr.isdigit():
            return 100
        else:
            return int(arr)

    def _normalize_train_response(train: dict, buff:int) -> dict:
        line = train['Line']
        destination = train['Destination']
        loc = train['LocationCode']
        arrival = train['Min']

        #MetroHero does fancy forecasting
        if ':' in arrival:
            arrival = str(train['minutesAway'])

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
