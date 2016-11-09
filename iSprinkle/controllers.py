from iSprinkle import *
from flask import jsonify, request


@app.route('/api/stations')
def stations():
    return jsonify(stations=iSprinkle.station_control.num_stations)


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
