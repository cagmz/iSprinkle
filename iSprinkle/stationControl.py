from dateutil.parser import parse
from dateutil.tz import tz


class StationControl(object):
    def __init__(self, stations, settings_handler):
        self.num_stations = stations
        self.user = settings_handler.get_settings_key('user')

        # instead of separate station id and status, use a dictionary
        # use dictionary.length instead of num_stations
        # self.station_status = {stationId: ON|OFF}
        self.station_status = {}
        self.reset_stations()

        # schedule dict is a parsed version of the watering schedule in settings.json
        # unparsed schedule is in SettingsHandler object
        self.schedule = {}
        self.set_schedule(settings_handler.get_schedule())

    def set_station(self, station, signal):
        self.station_status[station] = signal

    def reset_stations(self):
        for i in range(0, self.num_stations):
            self.set_station(i, False)

    def set_schedule(self, settings_json):
        # schedule dictionary:
        # (key) = (value) => (station, day) = (datetime in utc, watering duration)
        stations = settings_json['schedule']
        timezone_offset = settings_json['timezone_offset']
        for station in stations:
            for day in stations[station]:
                time_str = stations[station][day]['start_time'] + " " + timezone_offset
                # get 12 hour local time and and convert to 24 hour UTC time for use internally
                utc_time = string_to_utc(time_str)
                watering_duration = int(stations[station][day]['duration'])
                # print('{} starts at {} (UTC: {}) for {} min on {}'.format(station, time_str, utc_time, watering_duration, day))
                self.schedule.setdefault((station, day), []).append((utc_time, watering_duration))
            # print("finished with {}".format(station))
        print("StationControl instantiated with stations: {} ".format(self.station_status))


def string_to_utc(time_str):
    local_time = parse(time_str, fuzzy=True)
    utc_time = local_time.astimezone(tz.tzutc())
    return utc_time
