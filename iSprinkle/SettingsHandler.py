import os, json

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
            except OSError:
                raise OSError("SettingsHandler couldn't read settings file")
        else:
            # create default settings file
            print("Creating default settings file")
            # default timezone is -07:00
            default_settings = {"user": "New user", "timezone_offset": "-07:00",
                                "schedule": {"s0": {}, "s1": {}, "s2": {},
                                             "s3": {}, "s4": {}, "s5": {},
                                             "s6": {}, "s7": {}}}
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
        print(schedule)
        return schedule

    # test if key doesn't exist
    def set_key(self, key, value):
        # eg self.settings['schedule'] = schedule_json
        self.settings[key] = value

    # test various null and existing keys
    def get_key(self, key):
        value = None
        try:
            value = self.settings[key]
        except KeyError:
            pass
        return value
