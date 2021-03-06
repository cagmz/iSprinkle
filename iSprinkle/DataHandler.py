import os
import json
import sqlite3
import requests
import pickle
from datetime import datetime, timezone
from collections import OrderedDict

class DataHandler(object):
    def __init__(self, root_path):
        settings_file = '../data/settings.json'
        self.settings_path = os.path.join(root_path, settings_file)
        self.settings = {}
        self.load_settings()

        database_file = '../data/database.db'
        self.database_path = os.path.join(root_path, database_file)
        self.init_database()

        weather_cache_file = '../data/weather_cache.pkl'
        self.weather_cache_path = os.path.join(root_path, weather_cache_file)
        self.weather_cache = OrderedDict()
        self.load_weather_cache()

    # loads from filesystem
    def load_settings(self):
        if os.path.isfile(self.settings_path):
            try:
                with open(self.settings_path, 'r') as settings_file_handle:
                    self.settings = json.load(settings_file_handle)
                    print("Loaded existing settings file")
            except OSError:
                raise OSError("Couldn't read settings file")
        else:
            # create default settings file if one didn't exist
            print("Creating default settings file")

            utc_timezone_offset = datetime.now(timezone.utc).astimezone().strftime('%z')
            timezone_name = datetime.now(timezone.utc).astimezone().tzname()

            empty_weekly_schedule = {"Monday": {"start_times": []},
                                     "Tuesday": {"start_times": []},
                                     "Wednesday": {"start_times": []},
                                     "Thursday": {"start_times": []},
                                     "Friday": {"start_times": []},
                                     "Saturday": {"start_times": []},
                                     "Sunday": {"start_times": []}}

            default_settings = {
                "user": "New user",
                "location": {},
                "utc_timezone_offset": utc_timezone_offset,
                "timezone_name": timezone_name,
                "active_stations": [0, 1, 2, 3, 4, 5, 6, 7],
                "schedule": {"s0": {}, "s1": {}, "s2": {}, "s3": {},
                             "s4": {}, "s5": {}, "s6": {}, "s7": {}}
            }

            for station in default_settings['schedule'].keys():
                default_settings['schedule'][station] = empty_weekly_schedule

            self.settings = default_settings
            self.write_settings(default_settings)

    def write_settings(self, settings_json=None):
        if not settings_json:
            settings_json = self.settings

        try:
            with open(self.settings_path, 'w') as settings_file_handle:
                json.dump(settings_json, settings_file_handle)
                return True
        except OSError:
            raise OSError("Couldn't write settings file")

    def get_schedule(self):
        schedule = {'timezone_offset': self.get_settings_key('timezone_offset'),
                    'schedule': self.get_settings_key('schedule')}
        return schedule

    def get_settings_key(self, key):
        try:
            return self.settings[key]
        except KeyError:
            return "Error: key {} doesn't exist in the DataHandler settings".format(key)

    def set_settings_key(self, key, value):
        self.settings[key] = value

    def update_settings(self, data):
        for key, value in data.items():
            self.set_settings_key(key, value)

    def create_db_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.database_path)
        except sqlite3.Error as e:
            print('Unable to access database.\n{}'.format(e))

        return conn

    def init_database(self):
        if not os.path.isfile(self.database_path):
            conn = self.create_db_connection()
            conn.execute('''CREATE TABLE historical
                (datetime TEXT PRIMARY KEY NOT NULL,
                station INTEGER DEFAULT 0,
                fixed_duration INTEGER DEFAULT 0,
                forecasted_temp INTEGER DEFAULT 0,
                base_temp INTEGER DEFAULT 0,
                optimized_duration INTEGER DEFAULT 0,
                manual INTEGER DEFAULT 0);''')
            conn.commit()
            conn.close()
            print('Created new database')
        else:
            conn = sqlite3.connect(self.database_path)
            print('Loaded existing database')
            conn.close()

    def usage(self, start_date, end_date, stations):
        # TODO: build compound WHERE clause to include selected stations
        conn = self.create_db_connection()
        curr = conn.cursor()
        curr.execute('SELECT * FROM historical WHERE (datetime BETWEEN ? AND ?)', (start_date, end_date))
        rows = curr.fetchall()
        conn.close()
        return rows

    def insert_historical_record(self, args):
        """
        Executes an INSERT given a dictionary with keys:
        datetime, station, fixed_duration, forecasted_temp, base_temp, optimized_duration, manual
        :param args: a dictionary whose keys map directly to the historical table columns
        """

        conn = self.create_db_connection()
        curr = conn.cursor()

        """
        print('executing sql:\nINSERT INTO historical VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (args['datetime'], args['station'], args['fixed_duration'], args['forecasted_temp'],
                      args['base_temp'], args['optimized_duration'], args['manual']))
        """

        curr.execute('INSERT INTO historical VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (args['datetime'], args['station'], args['fixed_duration'], args['forecasted_temp'],
                      args['base_temp'], args['optimized_duration'], args['manual']))
        conn.commit()
        conn.close()

    def update_weather_cache(self):

        if len(self.settings['location']) == 0:
            print('Error: unable to update weather cache (missing location)')
            return

        # check weather cache for freshness. generate the a date range for the past 7 days, including today,
        # and make weather api request if needed

        key = ''
        latitude = '37.4226981' #self.settings['location']['lat']
        longitude = '-122.1686022'
        unix_time = 1480665600
        excluded_blocks = 'minutely,hourly'



        request = 'https://api.darksky.net/forecast/{}/{},{},{}?exclude={}'.format(key, latitude, longitude, unix_time, excluded_blocks)
        r = requests.get(request)

        today = []
        past_week = []

        # generate unix times for past 7 days, including today, and fetch weather forecasts for each


        # print(r.json())

    def load_weather_cache(self):
        if not os.path.isfile(self.weather_cache_path):
            with open(self.weather_cache_path, 'wb') as weather_cache_file:
                pickle.dump(self.weather_cache, weather_cache_file)
        else:
            with open(self.weather_cache_path, 'rb') as weather_cache_file:
                self.weather_cache = pickle.load(weather_cache_file)

        self.update_weather_cache()
