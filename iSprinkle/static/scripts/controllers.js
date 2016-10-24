iSprinkleApp.controller('HomeController',
    function DashboardController($scope) {
        // Dashboard
        // Call web api to retrieve and display historical data
        $scope.helloWorld = "HomeController";

        $scope.options = {
            chart: {
                type: 'lineChart',
                height: 450,
                margin: {
                    top: 20,
                    right: 20,
                    bottom: 40,
                    left: 55
                },
                x: function (d) {
                    return d.x;
                },
                y: function (d) {
                    return d.y;
                },
                useInteractiveGuideline: true,
                dispatch: {
                    stateChange: function (e) {
                        console.log("stateChange");
                    },
                    changeState: function (e) {
                        console.log("changeState");
                    },
                    tooltipShow: function (e) {
                        console.log("tooltipShow");
                    },
                    tooltipHide: function (e) {
                        console.log("tooltipHide");
                    }
                },
                xAxis: {
                    axisLabel: 'Time (ms)'
                },
                yAxis: {
                    axisLabel: 'Voltage (v)',
                    tickFormat: function (d) {
                        return d3.format('.02f')(d);
                    },
                    axisLabelDistance: -10
                },
                callback: function (chart) {
                    // console.log("!!! lineChart callback !!!");
                }
            },
            title: {
                enable: true,
                text: 'Title for Line Chart'
            },
            subtitle: {
                enable: true,
                text: 'Subtitle for simple line chart. Lorem ipsum dolor sit amet, at eam blandit sadipscing, vim adhuc sanctus disputando ex, cu usu affert alienum urbanitas.',
                css: {
                    'text-align': 'center',
                    'margin': '10px 13px 0px 7px'
                }
            },
            caption: {
                enable: true,
                html: '<b>Figure 1.</b> Lorem ipsum dolor sit amet, at eam blandit sadipscing, ' +
                '<span style="text-decoration: underline;">vim adhuc sanctus disputando ex</span>, ' +
                'cu usu affert alienum urbanitas. <i>Cum in purto erat, mea ne nominavi persecuti reformidans.</i> ' +
                'Docendi blandit abhorreant ea has, minim tantas alterum pro eu. <span style="color: darkred;">' +
                'Exerci graeci ad vix, elit tacimates ea duo</span>. Id mel eruditi fuisset. Stet vidit patrioque ' +
                'in pro, eum ex veri verterem abhorreant, id unum oportere intellegam nec<sup>[1, ' +
                '<a href="https://github.com/krispo/angular-nvd3" target="_blank">2</a>, 3]</sup>.',
                css: {
                    'text-align': 'justify',
                    'margin': '10px 13px 0px 7px'
                }
            }
        };

        $scope.data = sinAndCos();

        /*Random Data Generator */

        function sinAndCos() {
            var sin = [], sin2 = [],
                cos = [];

            //Data is represented as an array of {x,y} pairs.
            for (var i = 0; i < 100; i++) {
                sin.push({x: i, y: Math.sin(i / 10)});
                sin2.push({x: i, y: i % 10 == 5 ? null : Math.sin(i / 10) * 0.25 + 0.5});
                cos.push({x: i, y: .5 * Math.cos(i / 10 + 2) + Math.random() / 10});
            }

            //Line chart data should be sent as an array of series objects.
            return [
                {
                    values: sin,      //values - represents the array of {x,y} data points
                    key: 'Sine Wave', //key  - the name of the series.
                    color: '#ff7f0e',  //color - optional: choose your own line color.
                    strokeWidth: 2,
                    classed: 'dashed'
                },
                {
                    values: cos,
                    key: 'Cosine Wave',
                    color: '#2ca02c'
                },
                {
                    values: sin2,
                    key: 'Another sine wave',
                    color: '#7777ff',
                    area: true      //area - set to true if you want this line to turn into a filled area chart.
                }
            ];
        };

    });

iSprinkleApp.controller('ScheduleController', ['$scope', '$http', '$log', '$compile', 'StationFactory',
    function ScheduleController($scope, $http, $log, $compile, StationFactory) {

        $scope.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

        $scope.numberOfStations = -1;
        StationFactory.getNumberOfStations().then(function (response) {
            $scope.numberOfStations = response.data.stations;
            StationFactory.getSchedule().then(function (response) {

                $scope.scheduleData = response.data;
                $log.debug($scope.scheduleData.schedule);

                // view uses tableHeader to create table heading
                $scope.tableHeader = ['Stations'].concat($scope.weekdays);

                var rowInject = '<thead><tr><th ng-repeat="column in tableHeader">{{ column }}</th></tr></thead><tbody>';
                for (var station in $scope.scheduleData.schedule) {
                    // $log.debug(station);

                    // for each station (row), iterate through the weekdays and populate the cells
                    // each station may have a set time and duration
                    var stationSchedule = $scope.scheduleData.schedule[station];
                    var stationNumber = parseInt(station.substring(1)) + 1;
                    rowInject += "<tr><td>Station " + stationNumber + "</td>";

                    for (var day = 0; day < $scope.weekdays.length; day++) {
                        // dayInfo is an object with start time (string) and duration (int)
                        // eg 'Monday' {"start_time": "12:00 AM", "duration": 5}

                        var currentDay = $scope.weekdays[day];
                        var dayInfo = stationSchedule[currentDay];

                        rowInject += '<td><form class="schedule-cell">';
                        for (var start_time = 0; start_time < dayInfo.start_times.length; start_time++) {
                            rowInject += '<div class="form-group"><div class="input-group">';
                            var time = ['<label for="' + station + '_' + currentDay + '_startTime_' + start_time + '">Start:</label>',
                                '<input id="' + station + '_' + currentDay + '_startTime_' + start_time + '" ' +
                                'ng-model="scheduleData.schedule.' + station + '.' + currentDay + '.start_times[' + start_time + '].time' + '" ' +
                                'type="text" class="input-small">'].join('');
                            var duration = ['<label for="' + station + '_' + currentDay + '_duration_' + start_time + '">Time: </label>',
                                '<input id="' + station + '_' + currentDay + '_duration_' + start_time + '" ng-model="scheduleData.schedule.'
                                + station + '.' + currentDay + '.start_times[' + start_time + '].duration' + '" ' + 'type="number" min="0" class="input-small">'
                            ].join('');
                            rowInject += time + duration + '</div></div>'
                        }
                        rowInject += '</form></td>';
                    }
                    rowInject += "</tr>";
                }
                rowInject += "</tbody>";
                // $log.debug(rowInject);
                // must call compile so that Angular binds the injected JavaScript with the DOM
                $('#scheduleTable').append($compile(rowInject)($scope));
            });
        });

        $scope.saveSchedule = function saveSchedule() {
            // could use jQuery modal instead of alert
            $log.debug($scope.scheduleData);
            $log.debug($scope.scheduleData.schedule);

            // remove stations with 0 as duration
            for (var station in $scope.scheduleData.schedule) {
                var stationInfo = $scope.scheduleData.schedule[station];
                for (var i = 0; i < $scope.weekdays.length; i++) {
                    var day = $scope.weekdays[i];
                    var startTimes = stationInfo[day]['start_times'];
                    for (var j = 0; j < startTimes.length; j++) {
                        var start = startTimes[j];
                        if (start.duration === 0) {
                            startTimes.splice(j, 1);
                            j -= 1;
                        }
                    }
                }
            }

            // TODO: POST schedule and timezone offset
            $http.post('api/schedule', $scope.scheduleData).then(
                function (response) {
                    if (response.data.reply === 'Schedule saved') {
                        window.alert('Schedule saved');
                        window.location.reload(true);
                    } else {
                        errorCallback(response.data.reply);
                    }
                },
                errorCallback);

            function errorCallback(err) {
                err === undefined ? window.alert('Error saving schedule') : window.alert(err);
            }

        };

        $scope.validateWateringTime = function validateWateringTime(stations, duration, interval, startTime) {
            // Input validation
            if (!stations || !interval || !duration || !startTime) {
                window.alert('Please fill the entire form.');
                return;
            }

            duration = parseInt(duration);
            if (duration <= 0) {
                window.alert('Error: Duration must be a number greater than 0.');
                return;
            }

            var wateringDays = new Set();
            for (var i = 0; i < interval.length; i++) {
                if (interval[i] === 'every day') {
                    wateringDays = $scope.weekdays;
                    break;
                }
                else if (interval[i] === 'odd days') {
                    for (var j = 0; j < $scope.weekdays.length; j += 2) {
                        wateringDays.add($scope.weekdays[j]);
                    }
                }
                else if (interval[i] === 'even days') {
                    for (var j = 1; j < $scope.weekdays.length; j += 2) {
                        wateringDays.add($scope.weekdays[j]);
                    }
                } else {
                    wateringDays.add(interval[i]);
                }
            }

            // Convert to an array for easy indexing
            wateringDays = Array.from(wateringDays);

            $log.debug('wateringDays:');
            $log.debug(wateringDays);

            $log.debug('Stations:');
            $log.debug(stations);

            $log.debug('Duration:');
            $log.debug(duration);

            $log.debug('Interval:');
            $log.debug(interval);

            $log.debug('startTime:');
            $log.debug(startTime);

            var schedule = $scope.scheduleData.schedule;

            $log.debug('original schedule');
            $log.debug(schedule);

            for (var i = 0; i < stations.length; i++) {
                var stationId = 's' + i;
                $log.debug('Current station');
                $log.debug('\t' + stationId);
                for (var j = 0; j < wateringDays.length; j++) {
                    var day = wateringDays[j];
                    $log.debug('Current day');
                    $log.debug('\t' + day);
                    var newStartTime = {"duration": duration, "time": startTime};
                    $log.debug('Adding startTime');
                    $log.debug('\t' + startTime);
                    /*
                     Assume there are no overlaps in station start/end times for POC
                     But a check should be performed here
                     */
                    var overlap_station;
                    // check for overlaps
                    if (overlap_station) {
                        window.alert('Error: Station start time '
                            + startTime + ' conflicts with the current schedule');
                        return;
                    }
                    schedule[stationId][day]['start_times'].push(newStartTime);
                }
            }

            $log.debug('new Schedule');
            $log.debug($scope.scheduleData.schedule);

            $scope.saveSchedule();
        };

        $scope.timezone = function timezone() {
            // this function should be used to set the timezone before POSTing the schedule object to the server
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
