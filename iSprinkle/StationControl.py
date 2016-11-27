from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep
from datetime import datetime, timezone
from dateutil.parser import parse
from dateutil.tz import tz
from arrow import Arrow
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
        self.data_handler = data_handler
        self.watering = False

        # self.data_handler.get_schedule()['timezone_offset']
        self.utc_timezone_offset = datetime.now(timezone.utc).astimezone().strftime('%z')
        self.timezone_name = datetime.now(timezone.utc).astimezone().tzname()
        print('Operating in {} timezone ({})'.format(self.timezone_name, self.utc_timezone_offset))
        self.bg_scheduler = BackgroundScheduler()
        self.set_schedule(self.data_handler.get_schedule())

        if GPIO:
            atexit.register(self.cleanup)
            # GPIO.setwarnings(False)
            self.setup_gpio()

    def set_schedule(self, settings_json):
        self.bg_scheduler.remove_all_jobs()
        stations = settings_json['schedule']
        for station in stations:
            for day in stations[station]:
                for start_time in stations[station][day]['start_times']:
                    station_id = int(station[-1])
                    time_str = day + " " + start_time['time'] + " " + self.utc_timezone_offset
                    # get 12 hour time and convert to time-zone aware datetime object (24 hour UTC time) for use internally
                    utc_time = timestr_to_utc(time_str)
                    duration = int(start_time['duration'])
                    print('utc time is {}'.format(utc_time))
                    print('Station {} will start at {} for {} minutes'.format(station_id, utc_time, duration))
                    # TODO: set 'interval' trigger instead of 'date'.
                    # Jobs may exit scheduler after running once if the 'date' trigger is used
                    self.bg_scheduler.add_job(self.water, 'date', run_date=utc_time, args=[station_id, duration])
            print('Added start times for station {}'.format(station))
        
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
        # pause normal schedule
        jobs_paused = self.pause_schedule()

        start, last_duration_seconds = Arrow.utcnow(), 0
        start_buffer_seconds = 1

        print('Original start: {}'.format(start))
        # for every station, set a scheduling for the duration specified
        # stations are ran serially
        for station, duration in watering_request.items():
            station_id = int(station)
            job_start = start.replace(seconds=last_duration_seconds)
            print('Station {} will start at {} for {} minutes'.format(
                station, job_start.format('HH:mm:ssZZ'), duration))
            self.bg_scheduler.add_job(self.water, 'date', run_date=job_start.datetime,
                                      args=[station_id, duration])
            last_duration_seconds = duration * 60

        # reschedule the original schedule after all stations have watered
        print('start buffer in seconds is {}'.format(start_buffer_seconds))
        job_start = start.replace(seconds=last_duration_seconds + start_buffer_seconds)
        print('job start for resuming schedule is {}'.format(job_start.format('HH:mm:ssZZ')))

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
        print('GPIO setup successfully')

    def reset_stations(self):
        self.station_status = [False] * self.num_stations

    def cleanup(self):
        self.reset_stations()
        GPIO.cleanup()
        
    def water(self, station, duration):
        self.watering = True
        print('Station {} watering for {} min at {}'.format(station, duration, datetime.now().strftime('%c')))
                                                                                      
        # activate solenoid
        self.set_station(station, True)
        self.set_shift_register_values()
  
        # water and wait
        seconds = int(duration) * 60
        while seconds > 0:
            print('Drip.... second {}'.format(seconds))
            sleep(1)
            seconds -= 1
        
        # deactivate solenoid
        self.set_station(station, False)
        self.set_shift_register_values()
        
        print('Station {} finished watering'.format(station))
        self.watering = False


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
