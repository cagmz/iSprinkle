import os
import json


class SettingsHandler(object):
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.settings = {}
        self.load_settings(settings_path)

    # loads from filesystem
    def load_settings(self, settings_path):
        if os.path.isfile(settings_path):
            try:
                with open(settings_path, 'r') as settings_file_handle:
                    self.settings = json.load(settings_file_handle)
                    print("SettingsHandler loaded existing settings file")
            except OSError:
                raise OSError("SettingsHandler couldn't read settings file")
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
            raise OSError("SettingsHandler couldn't write settings file")

    def get_schedule(self):
        schedule = {'timezone_offset': self.get_settings_key('timezone_offset'),
                    'schedule': self.get_settings_key('schedule')}
        print(schedule)
        return schedule

    def get_settings_key(self, key):
        try:
            return self.settings[key]
        except KeyError:
            return "Error: key {} doesn't exist in the SettingsHandler settings".format(key)
