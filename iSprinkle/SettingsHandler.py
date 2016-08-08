import os
import json

# test if an existing file loads
# test if no file is present
#   test update settings
#   test load settings


class SettingsHandler(object):
    def __init__(self, settings_path):
        self.settings_path = settings_path
        self.settings = {}
        self.load_settings(settings_path)

    # loads from filesystem
    def load_settings(self, settings_path):
        if os.path.isfile(settings_path):
            # if settings file is in path, try to load it
            try:
                with open(settings_path, 'r') as settings_file_handle:
                    self.set_settings(json.load(settings_file_handle))
                    print("Loaded settings file")
            except OSError:
                raise OSError("SettingsHandler couldn't read settings file")
        else:
            # create default settings file
            print("Creating default settings file")
            # default timezone is -07:00
            default_settings = {
                "user": "New user",
                "timezone_offset": "-07:00",
                "schedule": {
                    "s0": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s1": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s2": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s3": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s4": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s5": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s6": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    },
                    "s7": {
                        "Monday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Tuesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Wednesday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Thursday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Friday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Saturday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        },
                        "Sunday": {
                            "start_time": "12:00 AM",
                            "duration": 0
                        }
                    }
                }
            }
            self.write_settings(default_settings)
            # use update_settings to save disk read
            self.set_settings(default_settings)

    def set_settings(self, settings_json):
        self.settings = settings_json

    def get_settings(self):
        return self.settings

    def write_settings(self, settings_json):
        try:
            with open(self.settings_path, 'w') as settings_file_handle:
                json.dump(settings_json, settings_file_handle)
        except OSError:
            raise OSError("SettingsHandler couldn't write settings file")

    def get_schedule(self):
        schedule = {'timezone_offset': self.get_key('timezone_offset'), 'schedule': self.get_key('schedule')}
        print("StationHandler's getSchedule() was called")
        print(schedule)
        return schedule

    # used to set the schedule from controllers.py
    # eg self.settings['schedule'] = scheduleData['schedule']
    def set_key(self, key, value):
        self.settings[key] = value
        return True

    def get_key(self, key):
        try:
            return self.settings[key]
        except KeyError:
            return "Error: key {} doesn't exist in the SettingsHandler settings".format(key)
