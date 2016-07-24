var iSprinkleApp = angular.module('iSprinkleApp', ['ngRoute']);

iSprinkleApp.config(['$routeProvider', '$logProvider', function($routeProvider, $logProvider) {
  // for debugging
  $logProvider.debugEnabled(true);

  // routes for controllers
  $routeProvider
  .when('/', {
    templateUrl: 'static/views/home/index.html',
    controller: 'HomeController'
  })
  .when('/home', {
    templateUrl: 'static/views/home/index.html',
    controller: 'HomeController'
  })
  .when('/schedule', {
    templateUrl: 'static/views/schedule/index.html',
    controller: 'ScheduleController'
  })
  .when('/admin', {
    templateUrl: 'static/views/admin/index.html',
    controller: 'AdminController'
  })
  .otherwise({
    redirectTo: '/'
  });
}]);
