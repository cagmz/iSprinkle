iSprinkleApp.factory('StationFactory', ['$http', '$log', function ($http, $log) {

  return {
    getNumberOfStations: function() {
      return $http.get('api/stations');
    },
    foo: function() {
      return -1;
    }
  }
  
}]);