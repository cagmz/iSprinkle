iSprinkleApp.controller('HomeController',
  function DashboardController($scope) {
    // Dashboard
    // Call web api to retrieve and display historical data
    $scope.helloWorld = "HomeController";
  });

iSprinkleApp.controller('ScheduleController', ['$scope', '$http', '$log', 'StationFactory',
  function ScheduleController($scope, $http, $log, StationFactory) {
    // use ng-repeat to create table and fill data
    $scope.header = ['Stations', 'Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday', 'Sunday'];

    // TODO: use API get request to get schedule, and use it to populate schedule
    $scope.numberOfStations = -1;
    StationFactory.getNumberOfStations().then(function (response) {
      $scope.numberOfStations = response.data.stations;
      $scope.stations = [];
      for (var i = 0; i < $scope.numberOfStations; i++) {
        $scope.stations.push(i + 1);
      }
    }).catch(function (err) {
      $log.debug("Unable to contact API");
    });
}]);

iSprinkleApp.controller('ManualController',
  function ManualController($scope) {
    $scope.helloWorld = "ManualController";
  });

iSprinkleApp.controller('AdminController',
  function AdminController($scope) {
    $scope.helloWorld = "AdminController";
  });
