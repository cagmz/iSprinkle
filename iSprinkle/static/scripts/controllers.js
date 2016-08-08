iSprinkleApp.controller('HomeController',
  function DashboardController($scope) {
    // Dashboard
    // Call web api to retrieve and display historical data
    $scope.helloWorld = "HomeController";
  });

iSprinkleApp.controller('ScheduleController', ['$scope', '$http', '$log', '$compile','StationFactory',
  function ScheduleController($scope, $http, $log, $compile ,StationFactory) {

    $scope.numberOfStations = -1;
    StationFactory.getNumberOfStations().then(function (response) {
      $scope.numberOfStations = response.data.stations;
      StationFactory.getSchedule().then(function (response) {

        $scope.scheduleData = response.data;
        $log.debug($scope.scheduleData);

        $scope.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
        // view uses tableHeader to create table heading
        $scope.tableHeader = ['Stations'].concat($scope.weekdays);

        // todo: try compiling & injecting one row at a time
        // todo: finalize injected markup and remove extra
        var rowInject = '<thead><tr><th ng-repeat="column in tableHeader">{{ column }}</th></tr></thead><tbody>';
        for (var station in $scope.scheduleData.schedule) {
          // $log.debug(station);

          // create a copy of weekdays array from index 0
          var tempWeekdays = $scope.weekdays.slice(0);
          // for each station (row), iterate through the weekdays and populate the cells
          // each station may have a set time and duration
          var stationSchedule = $scope.scheduleData.schedule[station];
          var stationNumber = station.substring(1);
          rowInject += "<tr><td>Station " + stationNumber + "</td>";

          for(var i = 0; i < $scope.weekdays.length; i++) {
            // dayInfo is an object with start time (string) and duration (int)
            // eg 'Monday' {"start_time": "12:00 AM", "duration": 5}

            var currentDay = $scope.weekdays[i];
            var dayInfo = stationSchedule[currentDay];
            var startTime = dayInfo['start_time'];
            var duration = dayInfo['duration'];

            var startTime = ['<label for="'+ station + '_startTime' + currentDay + '">Start:</label>',
              '            <input id="'+ station + '_startTime' + currentDay + '" + ng-model="scheduleData.schedule.' + station+ '.' + currentDay+ '.' + 'start_time" type="text" class="input-small">',
              '            <script type="text/javascript">',
              '            $("#' + station + '_startTime' + currentDay + '").timepicker({',
              '                defaultTime: false,',
              '                template: false,',
              '                showInputs: false,',
              '                minuteStep: 5',
              '            });',
              '        </script>',
              ''
            ].join('');

            // need to set listener for duration so that users can't enter negative number
            var duration = ['<label for="'+ station + '_duration">Time: </label>',
              '<input id="'+ station + '_duration" ng-model="scheduleData.schedule.' + station+ '.' + currentDay+ '.' + 'duration" type="number" min="0" class="input-small">'
            ].join('');
            rowInject += '<td><div class="form-group>"' + startTime + duration + '</div></td>';
          }
          rowInject += "</tr>";
          //debugger;
        }
        rowInject += "</tbody>";
        // $log.debug(rowInject);

        // must call compile so that Angular binds the injected Javscript with the DOM
        $('#scheduleTable').append($compile(rowInject)($scope));
      });
    });


    $scope.saveSchedule = function saveSchedule() {
      // could use jQuery modal instead of alert
      $log.debug('Called saveSchedule, sending the schedule...');
      $log.debug($scope.scheduleData);

      $http.post('api/schedule', $scope.scheduleData).then(
        function (response) {
          if(response.data.reply === 'Schedule saved') {
            window.alert('Schedule saved');
            $log.debug('Post successful');
          } else {
            errorCallback(response.data.reply);
          }},
        errorCallback);

      function errorCallback(err) {
        err === undefined ? window.alert('Error saving schedule') : window.alert(err);
      };

    };

}]);

iSprinkleApp.controller('ManualController',
  function ManualController($scope) {
    $scope.helloWorld = "ManualController";
});

iSprinkleApp.controller('AdminController',
  function AdminController($scope) {
    $scope.helloWorld = "AdminController";
});
