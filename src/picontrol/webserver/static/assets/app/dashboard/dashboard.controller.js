(function () {
    'use strict';
    angular.module('piAdmin.dashboard')
    .controller("DashboardController", DashboardController);

    DashboardController.$inject = ['$scope', '$rootScope', '$state', '$window', '$location', '$interval', 'DashboardService'];

    function DashboardController($scope, $rootScope, $state, $window, $location, $interval, DashboardService) {
        var vm = this;

        vm.cpu = { celsius: 0, fahrenheit: 0, fan: 'Off', cpuUsage:0, memUsage:0 };
        vm.chartTemps = { celsius: ['', '', '', '', '', '', '', '', '', ''], fahrenheit: ['', '', '', '', '', '', '', '', '', ''] };
        vm.chartUsage = { cpuUsage: ['', '', '', '', '', '', '', '', '', ''], memUsage: ['', '', '', '', '', '', '', '', '', ''] };

        vm.tempChart;
        vm.tempChartData = {};

        vm.usageChart;
        vm.usageChartData = {};

        $scope.timer;

        function getPiInfo() {
            DashboardService.getPiInfo(getCpuInfoSuccess, getCpuInfoError);
        }

        function getCpuInfoSuccess(response) {
            vm.cpu = response.data;
            updateChartData(vm.cpu.celsius, vm.cpu.fahrenheit, vm.cpu.cpuUsage, vm.cpu.memUsage);
        }

        function getCpuInfoError(response) {
            //handle error message
        }

        function initCharts() {
            vm.tempChartData = {
                labels: ['', '', '', '', '', '', '', '', '', ''],
                series: [
                   vm.chartTemps.celsius
                ]
            };

            var optionsTemp = {
                lineSmooth: false,
                low: 0,
                high: 200,
                showArea: false,
                height: "250px",
                axisX: {
                    showGrid: false,
                },
                lineSmooth: Chartist.Interpolation.simple({
                    divisor: 3
                }),
                showLine: true,
                showPoint: false,
            };

            var responsiveTemp = [
              ['screen and (max-width: 640px)', {
                  axisX: {
                      labelInterpolationFnc: function (value) {
                          return value[0];
                      }
                  }
              }]
            ];

            vm.tempChart = Chartist.Line('#chartCpuTemp', vm.tempChartData, optionsTemp, responsiveTemp);

            vm.usageChartData = {
                labels: ['', '', '', '', '', '', '', '', '', ''],
                series: [
                   vm.chartTemps.celsius
                ]
            };

            var optionsUsage = {
                lineSmooth: false,
                low: 0,
                high: 100,
                showArea: false,
                height: "250px",
                axisX: {
                    showGrid: false,
                },
                lineSmooth: Chartist.Interpolation.simple({
                    divisor: 3
                }),
                showLine: true,
                showPoint: false,
            };

            var responsiveUsage = [
              ['screen and (max-width: 640px)', {
                  axisX: {
                      labelInterpolationFnc: function (value) {
                          return value[0];
                      }
                  }
              }]
            ];

            vm.usageChart = Chartist.Line('#chartCpuUsage', vm.usageChartData, optionsUsage, responsiveUsage);
        }


        function updateChartData(celsius, fahrenheit, cpuUsage, memUsage) {
            //temp info
            for (var i = 0; i <= vm.chartTemps.celsius.length - 2; i++) {
                moveArrayItem(vm.chartTemps.celsius, i, i + 1);
            }
            for (var i = 0; i <= vm.chartTemps.fahrenheit.length - 2; i++) {
                moveArrayItem(vm.chartTemps.fahrenheit, i, i + 1);
            }

            vm.chartTemps.celsius[vm.chartTemps.celsius.length -1] = celsius;
            vm.chartTemps.fahrenheit[vm.chartTemps.fahrenheit.length -1] = fahrenheit;

            vm.tempChartData.series[0] = vm.chartTemps.fahrenheit;
            vm.tempChartData.series[1] = vm.chartTemps.celsius;

            vm.tempChart.update(vm.tempChartData);

            //usage info
            for (var i = 0; i <= vm.chartUsage.cpuUsage.length - 2; i++) {
                moveArrayItem(vm.chartUsage.cpuUsage, i, i + 1);
            }
            for (var i = 0; i <= vm.chartUsage.memUsage.length - 2; i++) {
                moveArrayItem(vm.chartUsage.memUsage, i, i + 1);
            }

            vm.chartUsage.cpuUsage[vm.chartUsage.cpuUsage.length - 1] = cpuUsage;
            vm.chartUsage.memUsage[vm.chartUsage.memUsage.length - 1] = memUsage;

            vm.usageChartData.series[0] = vm.chartUsage.cpuUsage;
            vm.usageChartData.series[1] = vm.chartUsage.memUsage;

            vm.usageChart.update(vm.usageChartData);
        }

        function moveArrayItem(array, from, to) {
            array.splice(to, 0, array.splice(from, 1)[0]);
        }

        function activate() {
            //get cpu info at 1 second intervals
            getPiInfo();
            $scope.timer = $interval(getPiInfo, 1000);

            initCharts();
        }

        $scope.$on("$destroy", function () {
            if (angular.isDefined($scope.timer)) {
                $interval.cancel($scope.timer);
            }
        });

        activate();
    }
})();