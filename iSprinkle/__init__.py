#!/usr/bin/python
from flask import Flask, g

app = Flask(__name__)
from iSprinkle.StationControl import StationControl
from iSprinkle.SettingsHandler import SettingsHandler

import iSprinkle.views, sqlite3, os, json, time

# local dev path
settings_file = '../data/settings.json'

# cloud 9 path
# settings_file = 'data/settings.json'

settings_path = os.path.join(app.root_path, settings_file)

station_control = None
settings_handler = None

MAX_STATIONS = 8

def create_settings_handler():
    global settings_handler, settings_path
    settings_handler = SettingsHandler(settings_path)


def create_station_control():
    global station_control
    station_control = StationControl(MAX_STATIONS, settings_handler)


def run_scheduler():
    global station_control
    print('Next job should run at {}'.format(str(station_control.watering_scheduler.next_run())))
    #while True:
    #    station_control.watering_scheduler.run_pending()
    #    time.sleep(1)

# Always run these
def setup():
    try:
        create_settings_handler()
        create_station_control()
        run_scheduler()
    except (RuntimeError, OSError) as e:
        print(e)
        # cleanup
        quit(0)

import iSprinkle.controllers
