iSprinkleApp.factory('StationFactory', ['$http', '$log', function ($http, $log) {

    return {
        getNumberOfStations: function () {
            return $http.get('api/stations');
        },
        getSchedule: function () {
            return $http.get('api/schedule');
        },
        currentlyWatering: function() {
            return $http.get('api/manual');
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