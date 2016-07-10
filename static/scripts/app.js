var iSprinkleApp = angular.module('iSprinkleApp', ['ngRoute']);

iSprinkleApp.config(['$routeProvider', function($routeProvider) {
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
