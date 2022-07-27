import time

from config import config
from secrets import secrets

class MetroApiOnFireException(Exception):
    pass

class MetroApi:
    def __init__(self):
        pass

    def fetch_train_predictions(self, wifi, station_codes, groups, walks={}) -> [dict]:
        return self._fetch_train_predictions(wifi, station_codes, groups, walks, retry_attempt=0)

    def _fetch_train_predictions(self, wifi, station_codes, groups, walks, retry_attempt: int) -> [dict]:
        try:
            print('Fetching...')
            start = time.time()

            if config['source_api'] == 'WMATA':
                # WMATA Method
                api_url = config['wmata_api_url'] + ','.join(set(station_codes))
                response = wifi.get(api_url, headers={'api_key': config['wmata_api_key']}, timeout=1).json()
                trains = list(filter(lambda t: (t['LocationCode'], t['Group']) in groups, response['Trains']))
            else:
                #Metro Hero Method
                trains = []
                for station in set(station_codes): # select trains in desired direction
                    api_url = config['metro_hero_api_url'].replace('[stationCode]', station)
                    response = wifi.get(api_url, headers={'apiKey': config['metro_hero_api_key']}, timeout = 30)
                    res = response.json()[:5]
                    response.close()
                    trains.extend(list(filter(lambda t: (station, t['Group']) in groups, res)))

            print('Received response from ' + config['source_api'] + ' api...')
            TIME_BUFFER = round((time.time() - start)/60) + 1
            trains = [self._normalize_train_response(t, TIME_BUFFER) for t in trains]

            if walks != {}:
                trains = list(filter(lambda t: self.arrival_map(t['arrival'])-walks[t['loc']] >= 0, trains))
                irint("a")

            if len(groups) > 1:
                trains = sorted(trains, key=lambda t: self.arrival_map(t['arrival']))

            print("Trains returned by api: ")
            for train in trains:
                print(train)
            print('Time to Update: ' + str(time.time() - start))
            return trains

        except Exception as e:
            print(e)
            if retry_attempt < config['metro_api_retries']:
                print('Failed to connect to API. Reattempting...')
                # Recursion for retry logic because I don't care about your stack
                return self._fetch_train_predictions(wifi, station_codes, groups, walks, retry_attempt + 1)
            else:
                raise MetroApiOnFireException()

    def arrival_map(self, arr):
        if arr == 'BRD':
            return 0
        elif arr == 'ARR':
            return 1
        elif not arr.isdigit():
            return 100
        else:
            return int(arr)

    def _normalize_train_response(self, train: dict, buff:int) -> dict:
        line = train['Line']
        destination = train['Destination']
        loc = train['LocationCode']

        if 'minutesAway' in train:
            arrival = round(float(train['minutesAway']))
        else:
            arrival = int(train["Min"])

        arrival = arrival - buff
        if arrival <= 0:
            arrival = 'ARR'
        else:
            arrival = str(arrival)

        if destination in config["station_mapping"]:
            destination = config["station_mapping"][destination]

        return {
            'line_color': self._get_line_color(line),
            'destination': destination[:config['destination_max_characters']],
            'arrival': arrival,
            'loc': loc
        }

    def _get_line_color(self, line: str) -> int:
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
