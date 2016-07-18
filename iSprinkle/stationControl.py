from dateutil.parser import parse
from dateutil.tz import tz

ON, OFF = 1, 0


class StationControl(object):
    def __init__(self, stations, settings_json):
        self.num_stations = stations
        self.station_ids = []

        for i in range(0, self.num_stations):
            self.station_ids.append(i)

        self.station_status = [OFF] * self.num_stations
        stations = settings_json['stations']

        # get station start times and watering duration
        # schedule dictionary:
        # (key) = (value) => (station, day) = (datetime in utc, watering duration)
        self.schedule = {}
        for station in stations:
            for day in stations[station]:
                time_str = stations[station][day]['start_time'] + " " + settings_json['timezone_offset']
                # get 24 hour local time and and convert to UTC time for use internally
                utc_time = string_to_utc(time_str)
                watering_duration = int(stations[station][day]['duration'])
                self.schedule.setdefault((station, day), []).append((utc_time, watering_duration))
            print("finished with {}".format(station))
        print("StationControl instantiated with stations: {} ".format(self.station_ids))

    def set_station(self, station, signal):
        if station in self.station_ids and signal in [OFF, ON]:
            self.station_status[station] = signal
            return True
        else:
            return False

    def reset_stations(self):
        self.stations_status = [OFF] * self.numStations


    # def write_settings(self, settings_

def string_to_utc(time_str):
    local_time = parse(time_str, fuzzy=True)
    print("local time: {}".format(local_time))
    utc_time = local_time.astimezone(tz.tzutc())
    print("utc time: {}".format(utc_time))
    return utc_time