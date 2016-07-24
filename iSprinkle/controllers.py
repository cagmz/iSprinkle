from iSprinkle import *
from flask import jsonify, request


@app.route('/api/stations')
def api():
    print("/api/stations hit")
    return jsonify(stations=iSprinkle.station_control.get_stations())


@app.route('/api/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        # send schedule to stationControl
        print("In api/schedule POST request")
        # iSprinkle.settings_handler.
        pass
    elif request.method == 'GET':
        station_schedules = iSprinkle.settings_handler.get_schedule()
        return jsonify(station_schedules)