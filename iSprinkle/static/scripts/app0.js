var iSprinkleApp = angular.module('iSprinkleApp', ['ngRoute']);

iSprinkleApp.config(function($routeProvider) {
  $routeProvider
  .when('/', {
    templateUrl: 'home/index.html',
    controller: 'HomeController'
  })
  .when('/home', {
    templateUrl: 'home/index.html',
    controller: 'HomeController'
  })
  .when('/schedule', {
    templateUrl: 'schedule/index.html',
    controller: 'ScheduleController'
  })
  .when('/admin', {
    templateUrl: 'admin/index.html',
    controller: 'AdminController'
  });
});
