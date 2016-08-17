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
        success = iSprinkle.settings_handler.set_key('schedule', stations)
        post_reply = {}
        if success:        # if schedule was saved in object and written to disk
            post_reply['reply'] = 'Schedule saved'
        else:
            post_reply['reply'] = 'Error saving schedule: Abducted by aliens'
        return jsonify(post_reply)
    elif request.method == 'GET':
        station_schedules = iSprinkle.settings_handler.get_schedule()
        return jsonify(station_schedules)