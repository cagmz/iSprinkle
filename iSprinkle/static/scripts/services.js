iSprinkleApp.factory('StationFactory', ['$http', '$log', function ($http, $log) {

    return {
        getNumberOfStations: function () {
            return $http.get('api/stations');
        },
        getSchedule: function () {
            return $http.get('api/schedule')
        },
        getUsage: function (startDate, endDate, stations) {
            var queryString = '?startDate=' + startDate +'&endDate=' + endDate + '&stations=' + stations;
            return $http.get('api/usage' + queryString)
        }
    }

}]);