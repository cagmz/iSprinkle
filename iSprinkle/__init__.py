#!/usr/bin/python
from flask import Flask, g

app = Flask(__name__)
from iSprinkle.StationControl import StationControl
import iSprinkle.views, sqlite3, os, json

settings_file = '../data/settings.json'
settings_path = os.path.join(app.root_path, settings_file)

station_control = None

MAX_STATIONS = 8

'''
database = '/data/database.db'


def setup_database():
    default_config = dict(DATABASE=os.path.join(app.root_path, database),
                          SECRET_KEY='development key', USERNAME='admin',
                          PASSWORD='default')
    app.config.update(default_config)


def connect_database():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """comments"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_database()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """more comments"""
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_database()
    return g.sqlite_db
'''


def check_settings():
    global settings_path
    # Create settings.json, raise exception if couldn't
    if not os.path.isfile(settings_path):
        print("Creating default settings file")
        # default timezone is -07:00
        default_settings = {"timezone_offset": "-07:00",
                            "stations": {"s0": {}, "s1": {}, "s2": {},
                                         "s3": {}, "s4": {}, "s5": {},
                                         "s6": {}, "s7": {}}}
        try:
            with open(settings_path, 'w') as settings_file_handle:
                json.dump(default_settings, settings_file_handle)
        except OSError:
            raise OSError("Couldn't create a new settings file")
    else:
        print("Found settings file")


def create_station_control():
    global station_control, settings_path
    try:
        with open(settings_path, 'r') as settings_file_handle:
            settings_json = json.load(settings_file_handle)
            station_control = StationControl(MAX_STATIONS, settings_json)
    except OSError:
        raise OSError("Error reading settings file")
    if station_control:
        print("Instantiated new StationControl object")
    else:
        raise RuntimeError("Couldn't instantiate new StationControl object")


# Always run these
def setup():
    try:
        check_settings()
        create_station_control()
    except (RuntimeError, OSError) as e:
        print(e)
        # cleanup
        quit(0)
