#!/usr/bin/python
from flask import Flask, g

app = Flask(__name__)
from iSprinkle.StationControl import StationControl
from iSprinkle.SettingsHandler import SettingsHandler

import iSprinkle.views
import os

# local dev path
settings_file = '../data/settings.json'
database_file = '../data/database.db'

# cloud 9 path
# settings_file = 'data/settings.json'

print('approot path: {}'.format(app.root_path))
settings_path = os.path.join(app.root_path, settings_file)
database_path = os.path.join(app.root_path, database_file)

station_control = None
settings_handler = None

MAX_STATIONS = 8


def create_settings_handler():
    global settings_handler, settings_path
    settings_handler = SettingsHandler(settings_path)


def create_station_control():
    global station_control
    station_control = StationControl(MAX_STATIONS, settings_handler)


# Always run these
def setup():
    try:
        create_settings_handler()
        create_station_control()
    except (RuntimeError, OSError) as e:
        print(e)
        # cleanup
        quit(0)

import iSprinkle.controllers
