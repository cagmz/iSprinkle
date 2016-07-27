iSprinkleApp.controller('HomeController',
  function DashboardController($scope) {
    // Dashboard
    // Call web api to retrieve and display historical data
    $scope.helloWorld = "HomeController";
  });

iSprinkleApp.controller('ScheduleController', ['$scope', '$http', '$log', 'StationFactory',
  function ScheduleController($scope, $http, $log, StationFactory) {

    $scope.numberOfStations = -1;
    StationFactory.getNumberOfStations().then(function (response) {
      $scope.numberOfStations = response.data.stations;
      StationFactory.getSchedule().then(function (response) {

        $scope.schedule = response.data;

        if ($scope.numberOfStations && $scope.schedule) {
          $log.debug($scope.numberOfStations);
          $log.debug($scope.schedule);
        }

        $scope.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        $scope.tableHeader = ['Stations'].concat($scope.weekdays);

        var scheduleTable = angular.element('#scheduleTable');
        debugger;
        $scope.cellInject = "";
        var l = 0, m = 0;
        for (var i = 0; i < $scope.weekdays.length; i++) {
          $scope.cellInject += "<tr><td>Station " + i;
          for (var j = 0; j < $scope.numberOfStations; j++, l++, m++) {
            var startTime = [
              '        <div class="bootstrap-timepicker">',
              '            <input id="startTime' + l + '" type="text" class="input-small">',
              '            <i class="icon-time"></i>',
              '        </div>',
              '        <script type="text/javascript">',
              '            $("#startTime' + l + '").timepicker({',
              '                template: false,',
              '                showInputs: false,',
              '                minuteStep: 5',
              '            });',
              '        </script>',
              ''
            ].join('');
            var duration = [
              '        <div class="bootstrap-timepicker">',
              '            <input id="duration' + m + '" type="text" class="input-small">',
              '            <i class="icon-time"></i>',
              '        </div>',
              '        <script type="text/javascript">',
              '            $("#startTime' + m + '").timepicker({',
              '                template: false,',
              '                showInputs: false,',
              '                minuteStep: 5',
              '            });',
              '        </script>',
              ''
            ].join('');
            $scope.cellInject += startTime + duration;
          }
          $scope.cellInject += "</td></tr>"
        }

            debugger;

      });
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
