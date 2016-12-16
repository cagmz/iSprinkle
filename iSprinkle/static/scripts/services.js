iSprinkleApp.factory('StationFactory', ['$http', '$log', function ($http, $log) {

    return {
        getNumberOfStations: function () {
            return $http.get('api/stations/all');
        },
        getSchedule: function () {
            return $http.get('api/schedule');
        },
        getActiveStations: function() {
            return $http.get('api/stations/active');
        },
        getUsage: function (startDate, endDate, stations) {
            var queryString = '?startDate=' + startDate + '&endDate=' + endDate + '&stations=' + stations;
            return $http.get('api/usage' + queryString);
        },
        getUptime: function () {
            return $http.get('api/rpi/uptime');
        },
        getLanIP: function () {
            return $http.get('api/rpi/ip');
        }
    }

}]);