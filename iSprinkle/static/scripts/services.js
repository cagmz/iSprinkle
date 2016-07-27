iSprinkleApp.factory('StationFactory', ['$http', '$log', function ($http, $log) {

  return {
    getNumberOfStations: function() {
      return $http.get('api/stations');
    },
    getSchedule: function() {
      return $http.get('api/schedule')
    }
  }
  
}]);