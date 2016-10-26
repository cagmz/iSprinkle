#!/usr/bin/python
from flask import Flask, g

app = Flask(__name__)
from iSprinkle.StationControl import StationControl
from iSprinkle.SettingsHandler import SettingsHandler

import iSprinkle.views
import os

# cloud 9 path
# settings_file = 'data/settings.json'

station_control = None
settings_handler = None

MAX_STATIONS = 8


def create_settings_handler():
    global settings_handler
    settings_handler = SettingsHandler(app.root_path)


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
