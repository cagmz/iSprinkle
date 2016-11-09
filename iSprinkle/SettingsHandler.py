import os
import json
import sqlite3
from dateutil import rrule, parser

class SettingsHandler(object):
    def __init__(self, root_path):
        settings_file = '../data/settings.json'
        self.settings_path = os.path.join(root_path, settings_file)
        self.settings = {}
        self.load_settings()

        database_file = '../data/database.db'
        self.database_path = os.path.join(root_path, database_file)
        self.init_database()

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
            # default timezone is -07:00
            default_settings = {
                "user": "New user",
                "timezone_offset": "-07:00",
                "schedule": {
                    "s0": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s1": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s2": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s3": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s4": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s5": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s6": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    },
                    "s7": {
                        "Monday": {"start_times": []},
                        "Tuesday": {"start_times": []},
                        "Wednesday": {"start_times": []},
                        "Thursday": {"start_times": []},
                        "Friday": {"start_times": []},
                        "Saturday": {"start_times": []},
                        "Sunday": {"start_times": []}
                    }
                }
            }
            self.settings = default_settings
            self.write_settings(default_settings)

    def write_settings(self, settings_json):
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
            return "Error: key {} doesn't exist in the SettingsHandler settings".format(key)

    def init_database(self):
        if not os.path.isfile(self.database_path):
            conn = sqlite3.connect(self.database_path)
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
        conn = sqlite3.connect(self.database_path)
        curr = conn.cursor()
        curr.execute('SELECT * FROM historical WHERE (datetime BETWEEN ? AND ?)', (start_date, end_date))
        rows = curr.fetchall()
        conn.close()
        return rows
