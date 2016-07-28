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

        $scope.cellInject = new Array($scope.numberOfStations);
        var l = 0, m = 0;
        for (var i = 0; i < $scope.numberOfStations; i++) {
          $scope.cellInject[i] = "<tr><td>Station " + i + "</td>";
          for (var j = 0; j < $scope.weekdays.length; j++, l++, m++) {
            var startTime = ['<label for="s' + l + 'startTime">Start:</label>',
              '            <input id="s' + l + '_startTime" type="text" class="input-small">',
              '            <script type="text/javascript">',
              '            $("#s' + l + '_startTime").timepicker({',
              '                defaultTime:\'12:00 AM\',',
              '                template: false,',
              '                showInputs: false,',
              '                minuteStep: 5',
              '            });',
              '        </script>',
              ''
            ].join('');
            var duration = ['<label for="s' + l + '_duration">Time:</label>',
              '            <input id="s' + m + '_duration" type="text" class="input-small" placeholder="HH:MM">',
              '            <script type="text/javascript">',
              '            $("#s' + m + '_duration").timepicker({',
              '                defaultTime:0,',
              '                template: false,',
              '                showMeridian: false,',
              '                showInputs: false,',
              '                minuteStep: 1',
              '            });',
              '        </script>',
              ''
            ].join('');
            $scope.cellInject[i] += "<td>" + startTime + duration + "</td>";
          }
          $scope.cellInject[i] += "</tr>"
          $('#scheduleTable > tbody').append($scope.cellInject[i]);
        }

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
