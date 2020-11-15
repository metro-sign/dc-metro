# DC Metro Board
import time

from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

REFRESH_INTERVAL = config['refresh_interval']
STATION_CODES = config['metro_station_code']
TRAIN_GROUPS = dict(zip(STATION_CODES, config['train_group']))
WALKING_TIMES = config['walking_time']
if max(WALKING_TIMES) == 0:
	WALKING_TIMES = {}
else:
	WALKING_TIMES = dict(zip(STATION_CODES, WALKING_TIMES))

def refresh_trains() -> [dict]:
	try:
		# trains = MetroApi.fetch_train_predictions(STATION_CODES, TRAIN_GROUPS)
		trains = MetroApi.fetch_train_predictions(STATION_CODES, TRAIN_GROUPS, WALKING_TIMES)
	except MetroApiOnFireException:
		print('WMATA Api is currently on fire. Trying again later ...')
		return None
	return trains

def sort_arrival_map(arr):
        if arr == '':
            return 100 #some large number to be sorted last
        elif arr == 'BRD' or arr == 'ARR':
            return 0 #If BRD or ARR, sort first
        else:
            return int(arr)

train_board = TrainBoard(refresh_trains)

while True:
	train_board.refresh()
	time.sleep(REFRESH_INTERVAL)
