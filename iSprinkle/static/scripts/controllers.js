iSprinkleApp.controller('HomeController', ['$scope', '$http', '$log', 'StationFactory',
    function HomeController($scope, $http, $log, StationFactory) {
        // Call web api to retrieve and display historical data

        $scope.getUsageData = function (startDate, endDate, stations) {
            var internalDateFormat = "YYYY-MM-DDTHH:mm:ssZ";

            if (startDate && endDate) {
                startDate = moment(startDate).utc().format(internalDateFormat);
                endDate = moment(endDate).utc().format(internalDateFormat);
            } else {
                if (!startDate) {
                    startDate = '1969-07-20T20:18:00+00:00';
                }
                if (!endDate) {
                    // set end date to today
                    endDate = moment.utc().format(internalDateFormat);
                }
            }

            if (!stations) {
                StationFactory.getNumberOfStations().then(function (response) {
                    var numberOfStations = response.data.stations;
                    stations = '';
                    for (var i = 1; i < numberOfStations; i++) {
                        stations += i + ',';
                    }
                    stations += numberOfStations;
                    $scope.makeUsageRequest(startDate, endDate, stations);
                }, function (error) {
                    window.alert('Error getting number of stations.');
                });
            }

            $scope.makeUsageRequest = function (startDate, endDate, stations) {
                StationFactory.getUsage(startDate, endDate, stations).then(function (response) {
                    /*
                     $log.debug('In makeUsageRequest()');
                     $log.debug('startDate');
                     $log.debug(startDate);
                     $log.debug('endDate');
                     $log.debug(endDate);
                     $log.debug('stations');
                     $log.debug(stations);
                     */

                    $scope.usageData = response.data;
                    $log.debug('Got data, processing for plotting...');
                    $log.debug($scope.usageData);
                    $scope.data = $scope.processUsageData($scope.usageData)
                }, function (error) {
                    window.alert('Error getting usage data');
                })
            };


            $scope.processUsageData = function () {
                /*
                 Usage data contains an array of watering data from startDate to endDate
                 [date, stationId, fixedDuration, forecastTemp, baseTemp, optimizedDuration, manual]
                 This function should return an array of plottable object where:
                 {x = date,
                 y = cumulative watering time of all stations that day and of previous days}
                 */

                var fixed_watering = [];
                var optimized_watering = [];
                var sum_fixed = 0;
                var sum_optimized = 0;

                for (var i = 0; i < $scope.usageData.length; i++) {
                    sum_fixed += $scope.usageData[i][2];
                    sum_optimized += $scope.usageData[i][5];
                    var plot_fixed = {x: $scope.usageData[i][0], y: sum_fixed};
                    fixed_watering.push(plot_fixed);
                    var plot_opt = {x: $scope.usageData[i][0], y: sum_optimized};
                    optimized_watering.push(plot_opt);
                }

                // $log.debug('fixed:');
                // $log.debug(fixed_watering);
                // $log.debug('opt:');
                // $log.debug(optimized_watering);

                // update size of chart before plotting
                $scope.options.chart.height = 450;
                return [{values: fixed_watering, key: 'Fixed', color: '#1b75ba'},
                    {values: optimized_watering, key: 'Optimized', color: '#26a874'}];
            };

        };

        /*
         * Options such as y-axis ticks should be set dynamically based on the # on the type of usage report requested.
         * Eg in a weekly report, report minutes (instead of hours)
         * */
        $scope.options = {
            chart: {
                type: 'lineChart',
                height: 100,
                margin: {
                    top: 20,
                    right: 75,
                    bottom: 40,
                    left: 75
                },
                noData: "Please select a date range.",
                x: function (d) {
                    /*
                     x axis values (dates) must be converted to UTC milliseconds
                     so d3 can use them
                     "2016-04-04T07:00:00+00:00" -> 1459753200000
                     */
                    return moment.utc(d.x).valueOf();
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
                    axisLabel: 'Date',
                    tickFormat: (function (d) {
                        return d3.time.format('%-m/%-d/%-Y')(new Date(d));
                    })
                },
                yAxis: {
                    axisLabel: 'Watering Time (Hours)',
                    tickFormat: (function (d) {
                        // convert minutes to hours for better scaling
                        return Math.trunc(d / 60);
                    })
                },
                callback: function (chart) {
                    $log.debug('It\'s aliiive!!');
                }
            },
            title: {
                enable: true,
                text: 'Watering Usage'
            },
            caption: {
                enable: false,
                html: '',
                css: {
                    'text-align': 'center',
                    'margin': '10px 13px 0px 7px'
                }
            }
        };

        $scope.data = [{"key": "", "values": []}];

    }]);

iSprinkleApp.controller('ScheduleController', ['$scope', '$http', '$log', '$compile', '$route', '$timeout', 'StationFactory',
    function ScheduleController($scope, $http, $log, $compile, $route, $timeout, StationFactory) {

        $scope.$on('$routeChangeStart', function (next, current) {
            // use this to update active navbar
        });

        $scope.weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

        $scope.numberOfStations = -1;
        StationFactory.getNumberOfStations().then(function (response) {
            $scope.numberOfStations = response.data.stations;
            StationFactory.getSchedule().then(function (response) {

                $scope.scheduleData = response.data;
                $log.debug($scope.scheduleData.schedule);

                // view uses tableHeader to create table heading dynamically
                $scope.tableHeader = ['Stations'].concat($scope.weekdays);

                var rowInject = '<thead><tr><th ng-repeat="column in tableHeader">{{ column }}</th></tr></thead><tbody>';
                for (var station in $scope.scheduleData.schedule) {
                    // $log.debug(station);

                    // for each station (row), iterate through the weekdays and populate the cells
                    // each station may have a set time and duration
                    var stationSchedule = $scope.scheduleData.schedule[station];
                    var stationNumber = parseInt(station.substring(1)) + 1;
                    rowInject += "<tr><td>" + stationNumber + "</td>";

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
                                'type="text" class="input-small"><br>'].join('');
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
                        $route.reload();
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

            /*
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
            */

            var schedule = $scope.scheduleData.schedule;

            /*
            $log.debug('original schedule');
            $log.debug(schedule);
            */

            for (var i = 0; i < stations.length; i++) {
                var stationId = 's' + stations[i];
                $log.debug('Current station');
                $log.debug('\t' + stationId);
                for (var j = 0; j < wateringDays.length; j++) {
                    var day = wateringDays[j];
                    // $log.debug('Current day');
                    // $log.debug('\t' + day);
                    var newStartTime = {"duration": duration, "time": startTime};
                    // $log.debug('Adding startTime');
                    // $log.debug('\t' + startTime);
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

            /*
            $log.debug('new Schedule');
            $log.debug($scope.scheduleData.schedule);
            */

            $scope.saveSchedule();
        };

    }]);

iSprinkleApp.controller('ManualController', ['$scope', '$http', '$log', '$route', '$timeout', 'StationFactory',
    function ManualController($scope, $http, $log, $route, $timeout, StationFactory) {

        $scope.$on('$viewContentLoaded', function () {
            $timeout(function () {
                // check if manual watering is in progress; if so, show progress bar in place of input
                $('.manualInputContainer').ready(function () {
                    $(".selectpicker").selectpicker({
                        style: 'btn-default',
                        noneSelectedText: 'None selected'
                    });
                });
            });
        });

        // can populate with user's 'active' stations instead
        $scope.stations = [];
        // use numberOfStations as sentinel for displaying error in UI if unable to contact api
        $scope.numberOfStations = -1;
        StationFactory.getNumberOfStations().then(function (response) {
            $scope.numberOfStations = response.data.stations;
            for (var i = 0; i < $scope.numberOfStations; i++) {
                var stationObject = {'id': i, 'duration': 0};
                $scope.stations.push(stationObject);
            }
        });

        $scope.validateManualWatering = function validateManualWatering() {
            var manualWaterRequest = {};
            for (var idx in $scope.stations) {
                var stationObj = $scope.stations[idx];
                if (stationObj.duration > 0) {
                    manualWaterRequest[stationObj.id] = stationObj.duration;
                }
            }

            if (Object.keys(manualWaterRequest).length === 0 && manualWaterRequest.constructor === Object) {
                window.alert('At least one station duration must be greater than 0.');
                return;
            }

            $log.debug(manualWaterRequest);

            $http.post('api/manual', manualWaterRequest).then(
                function (response) {
                    if (response.data.reply === 'Success') {
                        window.alert('Manual watering in progress... ');
                        // $route.reload();
                    } else {
                        errorCallback(response.data.reply);
                    }
                },
                errorCallback);

            function errorCallback(err) {
                err === undefined ? window.alert(err) : window.alert(err);
            }

            // use $route to force reload page after validating input and starting manual watering

        };

    }]);

iSprinkleApp.controller('AdminController', ['$scope', '$http', '$log', 'StationFactory',
    function AdminController($scope, $http, $log, StationFactory) {

        $scope.ip = 'Error finding LAN IP.';
        $scope.uptime = 'Error finding uptime.';

        $scope.refreshStatus = function refreshStatus() {
            StationFactory.getLanIP().then(
                function (response) {
                    $scope.ip = response.data;
                }, errorCallback);
            StationFactory.getUptime().then(
                function (response) {
                    $scope.uptime = response.data;
                }, errorCallback);
        };

        function errorCallback(err) {
            err === undefined ? window.alert('Error refreshing ' + err + '.') : window.alert(err);
        }

        $scope.refreshStatus();

    }]);
