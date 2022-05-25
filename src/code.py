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

# Get our username, key and desired timezone
aio_username = secrets.get("aio_username")
aio_key = secrets.get("aio_key")
location = secrets.get("timezone", None)
TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s" % (aio_username, aio_key)
TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z"

OFF_HOURS_ENABLED = aio_username and aio_key and config.get("display_on_time") and config.get("display_on_time")

REFRESH_INTERVAL = config['refresh_interval']
STATION_CODES = config['metro_station_codes']
TRAIN_GROUPS = list(zip(STATION_CODES, config['train_groups']))
WALKING_TIMES = config['walking_times']
if max(WALKING_TIMES) == 0:
    WALKING_TIMES = {}
else:
    WALKING_TIMES = dict(zip(STATION_CODES, WALKING_TIMES))

def is_off_hours() -> bool:
    now = wifi.get(TIME_URL).text
    now_hour = int(now[11:13])
    now_minute = int(now[14:16])
    after_end = now_hour > OFF_HOUR or (now_hour == OFF_HOUR and now_minute > OFF_MINUTE)
    before_start = now_hour < ON_HOUR or (now_hour == ON_HOUR and now_minute < ON_MINUTE)

    if ON_HOUR < OFF_HOUR or (ON_HOUR == OFF_HOUR and ON_MINUTE < OFF_MINUTE):
        return after_end or before_start
    else:
        return after_end and before_start

api = MetroApi()

def refresh_trains() -> [dict]:
    try:
         trains = api.fetch_train_predictions(wifi, STATION_CODES, TRAIN_GROUPS, WALKING_TIMES)
    except MetroApiOnFireException:
        print(config['source_api'] + ' API might be on fire. Resetting wifi ...')
        wifi.reset()
        return None
    return trains

train_board = TrainBoard(refresh_trains)

if OFF_HOURS_ENABLED:
    ON_HOUR, ON_MINUTE = map(int, config['display_on_time'].split(":"))
    OFF_HOUR, OFF_MINUTE = map(int, config['display_off_time'].split(":"))

while True:
    train_board.refresh()

    if OFF_HOURS_ENABLED:
        while is_off_hours():
	    train_board.turn_off_display()
            time.sleep(config['refresh_interval'])
	train_board.turn_on_display()

    time.sleep(REFRESH_INTERVAL)
