iSprinkleApp.controller('HomeController', 
  function DashboardController($scope) {
    // Dashboard
    
    $scope.helloWorld = "HomeController";
});

iSprinkleApp.controller('ScheduleController', 
  ['$scope', '$log', function ScheduleController($scope, $log) {
    $scope.$log = $log;
    
    // use ng-repeat to create table and fill data
    
    $scope.header = ['Stations', 'Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday', 'Sunday'];
    
    $scope.numberOfStations = 8;
    $scope.stations = [];
    for(var i = 0; i < $scope.numberOfStations; i++) {
      $scope.stations.push(i + 1);
    }
    
    $scope.helloWorld = "ScheduleController";
    
    $log.debug($scope.header);
    $log.debug($scope.stations);
}]);

iSprinkleApp.controller('ManualController', 
  function ManualController($scope) {
    $scope.helloWorld = "ManualController";
});

iSprinkleApp.controller('AdminController', 
  function AdminController($scope) {
    $scope.helloWorld = "AdminController";
});
