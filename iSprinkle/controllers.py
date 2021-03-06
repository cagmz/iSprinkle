from iSprinkle import *
from flask import jsonify, request


@app.route('/api/stations/all')
def all_stations():
    return jsonify(stations=iSprinkle.station_control.num_stations)


@app.route('/api/stations/active')
def active_stations():
    return jsonify(stations=iSprinkle.data_handler.settings['active_stations'])


@app.route('/api/settings', methods=['GET', 'POST'])
def settings():
    post_reply = {}
    if request.method == 'POST':
        updated_settings = request.get_json()
        iSprinkle.data_handler.update_settings(updated_settings)
        result = iSprinkle.data_handler.write_settings()
        if result:
            post_reply['reply'] = 'Success'
        else:
            post_reply['reply'] = 'Error saving settings'
        return jsonify(post_reply)
    elif request.method == 'GET':
        # settings for admin view
        post_reply = {'location': iSprinkle.data_handler.settings['location'],
                      'utc_timezone_offset': iSprinkle.data_handler.settings['utc_timezone_offset'],
                      'timezone_name': iSprinkle.data_handler.settings['timezone_name']}
        return jsonify(post_reply)


@app.route('/api/manual', methods=['GET', 'POST'])
def manual():
    if request.method == 'POST':
        manual_water_request = request.get_json()
        result = iSprinkle.station_control.manual_watering(manual_water_request)
        post_reply = {}
        if result:
            post_reply['reply'] = 'Success'
        else:
            post_reply['reply'] = 'Error manually watering'
        return jsonify(post_reply)
    elif request.method == 'GET':
        # check if manual watering is in progress
        # this is where a check for bgscheduler.pause() would be made
        return jsonify('To be implemented')


@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # replace the stations (and week/start/duration in each) inside the data_handler
        # schedule_data = {s0: {Monday: {}}, {Tuesday: {}}, etc}
        schedule_data = request.get_json()
        stations = schedule_data['schedule']
        iSprinkle.data_handler.settings['schedule'] = stations
        post_reply = {}
        try:
            # Update schedule in StationControl and update watering_scheduler jobs
            iSprinkle.data_handler.write_settings(iSprinkle.data_handler.settings)
            iSprinkle.station_control.set_schedule(iSprinkle.data_handler.settings)
            post_reply['reply'] = 'Schedule saved'
        except OSError:
            post_reply['reply'] = 'Error saving schedule: Abducted by aliens'
        return jsonify(post_reply)
    elif request.method == 'GET':
        station_schedules = iSprinkle.data_handler.get_schedule()
        return jsonify(station_schedules)


@app.route('/api/usage', methods=['GET'])
def usage():
    start_date = request.args.get('startDate').replace(' ', '+')
    end_date = request.args.get('endDate').replace(' ', '+')
    requested_stations = request.args.get('stations').split(',')
    records = iSprinkle.data_handler.usage(start_date, end_date, requested_stations)
    # todo: Preprocess records so that return is:
    # a dictionary with [date in utc milliseconds] -> array of rows on that day\

    # for record in records:
    #     record = list(record)
    #     record[0] = record[0][:10]

    return jsonify(records)


@app.route('/api/rpi/ip', methods=['GET'])
def lan():
    return jsonify(iSprinkle.utils.get_lan_ip())


@app.route('/api/rpi/restart', methods=['GET'])
def restart():
    return 'Rebooting'


@app.route('/api/rpi/uptime', methods=['GET'])
def reboot():
    return jsonify(iSprinkle.utils.uptime())
