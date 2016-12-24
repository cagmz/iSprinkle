import os
import json
import sqlite3
import requests
import pickle
import arrow
from datetime import timezone, datetime, date, timedelta
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
        self.weather_cache_size = 8
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

    def generate_weather_cache_dates(self):
        """
        Returns a list of date strings in the range between [today - weather_cache_size days, today]
        Strings are formatted to be used with Dark Sky API
        The date strings are sorted from latest -> earliest (today at index 0)
        """

        # generate the date objects for the past weather_cache_size days, including today
        today = date.today()
        past_dates = [today - timedelta(days=x) for x in range(self.weather_cache_size)]

        # convert date objects to strings in the format required for Dark Sky API
        past_dates = [arrow.get(d).format('YYYY-MM-DDTHH:mm:ss') for d in past_dates]
        return past_dates

    def update_weather_cache(self):

        if len(self.settings['location']) == 0:
            print('Error: unable to update weather cache (missing location)')
            return

        cached_dates = set(self.weather_cache.keys())

        past_dates = set(self.generate_weather_cache_dates())

        # create a set of dates in common between dates needed and those in cache
        common_dates = cached_dates & past_dates

        # a set of dates in dates_in_cache but not in past_week
        dates_to_request = past_dates - common_dates

        # delete stale dates from weather_cache (dates in cached_dates that are not in the past_dates)
        stale_dates = cached_dates - past_dates

        for old_date in stale_dates:
            del self.weather_cache[old_date]

        print('Need to request the following dates: {}'.format(dates_to_request))

        llave = 'd2b86bb26ffc7100739f5769527af4ad'
        latitude = self.settings['location']['lat']
        longitude = self.settings['location']['lng']

        # only request 'daily' data block from API
        excluded_blocks = 'currently,minutely,hourly,alerts,flags'

        for forecast_date in dates_to_request:
            request = 'https://api.darksky.net/forecast/{}/{},{},{}?exclude={}'.format(llave, latitude, longitude,
                                                                                       forecast_date, excluded_blocks)
            response = requests.get(request)

            if not response.ok:
                print('Failed to fetch forecast for date '.format(forecast_date))
                continue

            forecast = response.json()['daily']['data'][0]
            if forecast:
                print('Got forecast for date {}'.format(forecast_date))
                self.weather_cache[forecast_date] = forecast

        self.write_weather_cache()

    def write_weather_cache(self):
        with open(self.weather_cache_path, 'wb') as weather_cache_file:
            pickle.dump(self.weather_cache, weather_cache_file)

    def load_weather_cache(self):
        if not os.path.isfile(self.weather_cache_path):
            self.write_weather_cache()
        else:
            with open(self.weather_cache_path, 'rb') as weather_cache_file:
                self.weather_cache = pickle.load(weather_cache_file)

        self.update_weather_cache()
