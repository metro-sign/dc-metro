# DC Metro Board
import time
from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

from secrets import secrets
import busio
import board
from digitalio import DigitalInOut
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

# New network
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

REFRESH_INTERVAL = config['refresh_interval']
STATION_CODES = config['metro_station_code']
TRAIN_GROUPS = list(zip(STATION_CODES, config['train_group']))
WALKING_TIMES = config['walking_time']
if max(WALKING_TIMES) == 0:
	WALKING_TIMES = {}
else:
	WALKING_TIMES = dict(zip(STATION_CODES, WALKING_TIMES))

def refresh_trains() -> [dict]:
	try:
		trains = MetroApi.fetch_train_predictions(wifi, STATION_CODES, TRAIN_GROUPS, WALKING_TIMES)
	except MetroApiOnFireException:
		print('WMATA API might be on fire. Resetting wifi ...')
		wifi.reset()
		return None
	return trains

train_board = TrainBoard(refresh_trains)

while True:
	train_board.refresh()
	time.sleep(REFRESH_INTERVAL)
