from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.parser import parse
from dateutil.tz import tz
import datetime
import atexit

GPIO = None
try:
    import RPi.GPIO as GPIO
except ImportError:
    print('Error: Unable to import RPi.GPIO module (watering function disabled).')


class StationControl(object):

    # GPIO Pins (BCM numbering). OSPI uses 4 pins for shift register.
    clock_pin = 4
    out_pin = 17
    data_pin = 27
    latch_pin = 22

    def __init__(self, stations, data_handler):
        self.num_stations = stations
        self.station_status = [False] * self.num_stations

        if GPIO:
            atexit.register(self.cleanup)
            # GPIO.setwarnings(False)
            self.setup_gpio()

        # schedule dict is a parsed version of the watering schedule in settings.json
        # unparsed schedule is in SettingsHandler object
        self.schedule = {}
        self.watering_scheduler = BackgroundScheduler()
        self.set_schedule(data_handler.get_schedule())

    def set_schedule(self, settings_json):
        # schedule dictionary:
        # (key) = (value) => (station, day) = (datetime in utc, watering duration)

        self.watering_scheduler.remove_all_jobs()

        stations = settings_json['schedule']
        timezone_offset = settings_json['timezone_offset']
        for station in stations:
            for day in stations[station]:
                for start_time in stations[station][day]['start_times']:
                    time_str = start_time['time'] + " " + timezone_offset
                    # get 12 hour time and convert to time-zone aware datetime object (24 hour UTC time) for use internally
                    utc_time = timestr_to_utc(time_str)

                    duration = int(start_time['duration'])

                    # add all stations to the static schedule, but only add a watering job to the watering schedule
                    # if actually watering (duration > 0)
                    self.schedule.setdefault((station, day), []).append((utc_time, duration))
                    if duration > 0:
                        self.watering_scheduler.add_job(water, 'date', run_date=utc_time, args=[station, time_str, duration])
            print('Added water_schedule jobs for {}'.format(station))
        # start the scheduler if it's not already running
        if not self.watering_scheduler.state:
            self.watering_scheduler.start()

    def set_station(self, station, signal):
        self.station_status[station] = signal

    def reset_stations(self):
        self.station_status = [False] * self.num_stations

    def set_shift_register_values(self):
        if not GPIO:
            print('Error: set_shift_register_values() doesn\'t have GPIO module')
            return
        GPIO.output(StationControl.clock_pin, False)
        GPIO.output(StationControl.latch_pin, False)
        for station in range(0, self.num_stations):
            GPIO.output(StationControl.clock_pin, False)
            GPIO.output(StationControl.data_pin, self.station_status[self.num_stations - 1 - station])
            GPIO.output(StationControl.clock_pin, True)
        GPIO.output(StationControl.latch_pin, True)

    def toggle_shift_register_output(self, value):
        if value:
            GPIO.output(StationControl.out_pin, False)
        else:
            GPIO.output(StationControl.out_pin, True)

    def setup_gpio(self):
        if not GPIO:
            print('Error: setup_gpio() doesn\'t have GPIO module')
            return

        print('Setting up GPIO')
        # clean up after any previous applications
        GPIO.cleanup()
        # setup GPIO pins to interface with shift register
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(StationControl.clock_pin, GPIO.OUT)
        GPIO.setup(StationControl.out_pin, GPIO.OUT)
        self.toggleShiftRegisterOutput(False)
        GPIO.setup(StationControl.data_pin, GPIO.OUT)
        GPIO.setup(StationControl.latch_pin, GPIO.OUT)
        self.setShiftRegisterValues()
        self.toggleShiftRegisterOutput(True)

    def cleanup(self):
        self.reset_stations()
        GPIO.cleanup()

def water(station='-1', scheduled_time='23:59', duration='-1'):
    import time
    print('water(station={}, scheduled_time={}, duration={}), time_now = {}'.format(station, scheduled_time, duration, str(datetime.datetime.now())))

    # activate solenoid
    # TODO: watering must be done serially. Enforce this constraint client-side
    seconds = int(duration) * 60
    while seconds > 0:
        print('drip.... second {}'.format(seconds))
        time.sleep(1)
        seconds -= 1
    print('Station {} finished watering'.format(station))


def timestr_to_utc(time_str, local=True):
    """
    Converts a time string to 24 hour time.
    If local=True, time_str should contain a timezone offset and the caller should expect a localized datetime.
        eg  2016-10-25 07:00:00+00:00
            year-mo-da 24hr:min:sec+timezone_offset
    time_str can also contain dates
        in: timestr_to_utc('1/1/16 12:00 AM -07:00')
        out: 2016-01-01 07:00:00+00:00 (datetime)
    Else, time_str should not contain an offset, and the caller should expect a non-localized datetime.
    """
    if local:
        local_time = parse(time_str, fuzzy=True)
        utc_time = local_time.astimezone(tz.tzutc())
        return utc_time
    else:
        return parse(time_str)
