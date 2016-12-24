from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from datetime import datetime, timezone
from dateutil.parser import parse
from dateutil.tz import tz
from arrow import Arrow
from pytz import utc
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

    def __init__(self, data_handler):
        self.data_handler = data_handler
        self.station_status = {station_id: False for station_id in data_handler.settings['active_stations']}
        self.active_stations = data_handler.settings['active_stations']
        self.num_stations = len(self.station_status)

        self.utc_timezone_offset = self.data_handler.settings['utc_timezone_offset']
        self.timezone_name = self.data_handler.settings['timezone_name']
        print('Operating in {} timezone ({})'.format(self.timezone_name, self.utc_timezone_offset))
        self.bg_scheduler = BackgroundScheduler(timezone=utc)
        self.set_schedule(self.data_handler.get_schedule())

        if GPIO:
            atexit.register(self.cleanup)
            # GPIO.setwarnings(False)
            self.setup_gpio()

    def set_schedule(self, settings_json):
        self.bg_scheduler.remove_all_jobs()
        stations = settings_json['schedule']
        for station in stations:
            station_id = int(station[-1])
            if station_id not in self.active_stations:
                continue

            for day in stations[station]:
                for start_time in stations[station][day]['start_times']:
                    time_str = day + " " + start_time['time'] + " " + self.utc_timezone_offset
                    # convert to 12 hour time to time-zone aware datetime object (24 hour UTC time) for use internally
                    utc_time = timestr_to_utc(time_str)
                    fixed_duration = int(start_time['duration'])
                    print('Station {} will start at {} UTC for {} minutes'.format(station_id, utc_time, fixed_duration))
                    args = {'datetime': str(utc_time).replace(' ', 'T'), 'station': station_id,
                            'fixed_duration': fixed_duration, 'manual': 0}
                    self.bg_scheduler.add_job(self.water, 'interval', days=7, start_date=utc_time, args=[args])

        # start the scheduler if it's not already running
        if not self.bg_scheduler.state:
            self.bg_scheduler.start()

    def pause_schedule(self):
        print('Pausing schedule...')
        jobs_paused = 0
        for job in self.bg_scheduler.get_jobs():
            job.pause()
            print('Paused job {}'.format(job))
            jobs_paused += 1
        return jobs_paused

    def resume_schedule(self):
        print('Resuming schedule...')
        for job in self.bg_scheduler.get_jobs():
            job.resume()
            print('Resumed job {}'.format(job))
        print('Resumed schedule')

    def manual_watering(self, watering_request):
        """
        Pause existing schedule jobs and create a new watering job for every station in watering request.
        Water jobs are executed serially.
        """

        jobs_paused = self.pause_schedule()

        start, last_duration_seconds = Arrow.utcnow(), 5
        start_buffer_seconds = 5

        for station, duration in watering_request.items():
            station_id = int(station)
            job_start = start.replace(seconds=last_duration_seconds)

            dt = job_start.format('YYYY-MM-DDTHH:mm:ssZZ').replace('-00:00', '+00:00')
            args = {'datetime': dt, 'station': station_id, 'fixed_duration': duration, 'manual': 1}
            self.bg_scheduler.add_job(self.water, 'date', run_date=job_start.datetime, args=[args])

            last_duration_seconds = duration * 60

        # reschedule the original schedule after all stations have watered
        job_start = start.replace(seconds=last_duration_seconds + start_buffer_seconds)
        self.bg_scheduler.add_job(self.resume_schedule, 'date', run_date=job_start.datetime)

        # check if schedule contains: paused jobs, manual watering jobs, and extra job to resume paused jobs
        if len(self.bg_scheduler.get_jobs()) == (jobs_paused + len(watering_request) + 1):
            return True

        return False

    def set_station(self, station, signal):
        """
        Sets station [0,..., 7] to True or False (On | Off) in memory.
        Use set_shift_register_values() to activate GPIO
        """
        self.station_status[station] = signal

    def set_shift_register_values(self):
        """
        Activates GPIO based on self.station_status values
        """
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

        # setup GPIO pins to interface with shift register
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(StationControl.clock_pin, GPIO.OUT)
        GPIO.setup(StationControl.out_pin, GPIO.OUT)
        self.toggle_shift_register_output(False)
        GPIO.setup(StationControl.data_pin, GPIO.OUT)
        GPIO.setup(StationControl.latch_pin, GPIO.OUT)
        self.set_shift_register_values()
        self.toggle_shift_register_output(True)
        self.reset_stations()
        print('GPIO setup successfully')

    def reset_stations(self):
        self.station_status = [False] * self.num_stations

    def cleanup(self):
        self.reset_stations()
        GPIO.cleanup()

    def optimize_duration(self, fixed_duration):
        optimized, forecasted_temp, base_temp = fixed_duration, 70, 75

        # call data handler and get historical for last 7 days, inc. today
        # if it rained today, don't water, return 0

        # else return int(forecasted_temp * (fixed_duration/avg_temp))

        return optimized, forecasted_temp, base_temp

    def water(self, args):
        """
        args parameter contains a dict with args that are necessary for watering (station, duration).
        other args are for optimizing the duration (fixed_duration)
        the return values from optimize_duration will also be inserted into the dict
        args will be passed to data_handler for insertion; all keys map directly to columns in the historical table
        :param args: dictionary with keys 'datetime', 'station', 'fixed_duration', 'manual'
        """
        station = args['station']
        fixed_duration = args['fixed_duration']

        optimized_duration, forecasted_temp, base_temp = self.optimize_duration(fixed_duration)

        print('Station {} watering for {} min at {}'.format(station, optimized_duration, datetime.now().strftime('%c')))

        # activate solenoid
        self.set_station(station, True)
        self.set_shift_register_values()

        # water and wait
        seconds = int(optimized_duration) * 60
        while seconds > 0:
            print('Drip.... second {}'.format(seconds))
            sleep(1)
            seconds -= 1

        # deactivate solenoid
        self.set_station(station, False)
        self.set_shift_register_values()

        print('Station {} finished watering'.format(station))

        # add a few more k, v pairs before passing to data_handler for building a SQL insert statement
        args['forecasted_temp'] = forecasted_temp
        args['base_temp'] = base_temp
        args['optimized_duration'] = optimized_duration

        # send args to data handler for insertion to db
        self.data_handler.insert_historical_record(args)


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
