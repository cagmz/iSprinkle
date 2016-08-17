from iSprinkle import *
from flask import jsonify, request


@app.route('/api/stations')
def api():
    print("/api/stations hit")
    return jsonify(stations=iSprinkle.station_control.get_stations())


@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # replace the stations (and week/start/duration in each) inside the settings_handler
        # schedule_data = {s0: {Monday: {}}, {Tuesday: {}}, etc}
        schedule_data = request.get_json()
        stations = schedule_data['schedule']
        iSprinkle.settings_handler.settings['schedule'] = stations
        post_reply = {}
        try:
            iSprinkle.settings_handler.write_settings(iSprinkle.settings_handler.settings)
            post_reply['reply'] = 'Schedule saved'
        except OSError:
            post_reply['reply'] = 'Error saving schedule: Abducted by aliens'
        return jsonify(post_reply)
    elif request.method == 'GET':
        station_schedules = iSprinkle.settings_handler.get_schedule()
        return jsonify(station_schedules)