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

        var rowInject = '<thead><tr><th ng-repeat="column in tableHeader">{{ column }}</th></tr></thead><tbody>';
        for (var station in $scope.scheduleData.schedule) {
          $log.debug(station);
          // create a copy of weekdays array from index 0
          var tempWeekdays = $scope.weekdays.slice(0);
          // for each station (row), iterate through the weekdays and populate the cells
          // each station may have a set time and duration
          var stationSchedule = $scope.scheduleData.schedule[station];
          var stationNumber = station.substring(1);
          rowInject += "<tr><td>Station " + stationNumber + "</td>";
          // debugger;
          for(var i = 0; i < $scope.weekdays.length; i++) {
            // dayInfo is an object with start time (string) and duration (int)
            // eg 'Monday' {"start_time": "12:00 AM", "duration": 5}
            //debugger;
            var currentDay = $scope.weekdays[i];
            var dayInfo = stationSchedule[currentDay];
            var startTime = dayInfo['start_time'];
            var duration = dayInfo['duration'];

            var startTime = ['<label for="'+ station + '_startTime">Start:</label>',
              //'            <input id="'+ station + '_startTime" type="text" class="input-small">',
              '            <input id="'+ station + '_startTime" ng-model="scheduleData.schedule.' + station+ '.' + currentDay+ '.' + 'start_time" type="text" class="input-small">',
              //'            <script type="text/javascript">',
              //'            $("#' + station + '_startTime").timepicker({',
              //'                defaultTime:\'' + dayInfo['start_time'] + '\',',
              //'defaultTime: false,',
              //'                template: false,',
              //'                showInputs: false,',
              //'                minuteStep: 5',
              //'            });',
              //'        </script>',
              //''
            ].join('');
            var duration = ['<label for="'+ station + '_duration">Time:</label>',
              '            <input id="'+ station + '_duration" type="text" class="input-small" placeholder="HH:MM">',
              '            <script type="text/javascript">',
              '            $("#' + station + '_duration").timepicker({',
              // '                defaultTime:' + dayInfo['duration'] +',',
              '                defaultTime:0,',
              '                template: false,',
              '                showMeridian: false,',
              '                showInputs: false,',
              '                minuteStep: 1',
              '            });',
              '        </script>',
              ''
            ].join('');
            rowInject += "<td>" + startTime + duration + "</td>";
          }
          rowInject += "</tr>";
          //debugger;
        }
        rowInject += "</tbody>";
        $log.debug(rowInject);
        // must call compile so that Angular binds the injected Javscript with the DOM
        $('#scheduleTable').append($compile(rowInject)($scope));
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
