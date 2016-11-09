from flask import Flask, g

app = Flask(__name__)

from iSprinkle.StationControl import StationControl
from iSprinkle.DataHandler import DataHandler

import iSprinkle.views
import iSprinkle.utils

station_control = None
data_handler = None

MAX_STATIONS = 8


# Always run these
def setup():
    try:
        global data_handler, station_control
        data_handler = DataHandler(app.root_path)
        station_control = StationControl(MAX_STATIONS, data_handler)
    except (RuntimeError, OSError) as e:
        print(e)
        # cleanup
        quit(0)

import iSprinkle.controllers
