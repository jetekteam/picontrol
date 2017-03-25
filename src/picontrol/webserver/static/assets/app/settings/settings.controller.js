(function () {
    'use strict';
    angular.module('piAdmin.settings')
    .controller("SettingsController", SettingsController);

    SettingsController.$inject = ['$scope', '$rootScope', '$state', '$window', '$location', '$interval', 'SettingsService', 'ModalService', 'AlertService', 'AppService', 'DashboardService'];

    function SettingsController($scope, $rootScope, $state, $window, $location, $interval, SettingsService, ModalService, AlertService, AppService, DashboardService) {
        var vm = this;

        vm.alerts = [];
        vm.fanConfig = { thresholdOn: 0, thresholdOff: 0, interval: 0 };
        vm.buttonOption = 0;

        vm.setFanConfig = setFanConfig;
        vm.setButtonConfig = setButtonConfig;

        vm.updateInterval = updateInterval;
        vm.updateThresholdOn = updateThresholdOn;
        vm.updateThresholdOff = updateThresholdOff;

        vm.getVersion = getVersion;
        vm.checkUpdate = checkUpdate;

        vm.version = {'number':'1.01','date':''}

        vm.cpu = { celsius: 0, fahrenheit: 0, fan: 'Off', cpuUsage:0, memUsage:0 };

        function updateThresholdOn(slider) {
            vm.fanConfig.thresholdOn = slider.from;
        }

        function updateThresholdOff(slider) {
            vm.fanConfig.thresholdOff = slider.from;
        }

        function updateInterval(slider) {
            vm.fanConfig.interval = slider.from;
        }

        function clearAlerts() {
            vm.alerts = [];
        }

        function getPiInfo() {
            DashboardService.getPiInfo(getCpuInfoSuccess, getCpuInfoError);
        }

        function getCpuInfoSuccess(response) {
            vm.cpu = response.data;
        }

        function getCpuInfoError(response) {
            //handle error message
        }

        function setFanConfig() {
            AppService.setLoaderVisible(true);
            SettingsService.setFanConfig(vm.fanConfig, setFanConfigSuccess, setFanConfigError);
        }

        function setFanConfigSuccess(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message','Fan Configuration saved successfully.','Close');
        }

        function setFanConfigError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message','Unable to save Fan Configuration.','Close');
        }

        function getFanConfig() {
            SettingsService.getFanConfig(getFanConfigSuccess, getFanConfigError);
        }

        function getFanConfigSuccess(response) {
            vm.fanConfig = response.data;
        }

        function getFanConfigError(response) {

        }

        function setButtonConfig() {
            AppService.setLoaderVisible(true);
            SettingsService.setButtonConfig(vm.buttonOption, setButtonConfigSuccess, setButtonConfigError);
        }

        function setButtonConfigSuccess(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message','Button Configuration saved successfully, changes will take effect on reboot.','Close');
        }

        function setButtonConfigError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message','Unable to save Button Configuration.','Close');
        }

        function getButtonConfig() {
            SettingsService.getButtonConfig(getButtonConfigSuccess, getButtonConfigError);
        }

        function getButtonConfigSuccess(response) {
            vm.buttonOption = response.data.option;
        }

        function getButtonConfigError(response) {

        }

        function getVersion() {
            SettingsService.getVersion(getVersionSuccess, getVersion);
        }

        function getVersionSuccess(response) {
            vm.version = response.data;
        }

        function getVersionError(response) {

        }

        function checkUpdate() {
            AppService.setLoaderVisible(true);
            SettingsService.checkUpdate(checkUpdateSuccess, checkUpdateError);
        }

        function checkUpdateSuccess(response) {
            AppService.setLoaderVisible(false);
            var updateInfo = response.data.update;
            try {
                if (updateInfo == false) {
                    AlertService.alert('Message','No updates found.','Close');
                }
                else {
                    ModalService.showModal({
                        templateUrl: 'static/assets/app/settings/modal/update.html',
                        controller: 'UpdateController',
                        controllerAs: 'updateCtrl'
                    }).then(function (modal) {
                        modal.element.modal();
                        modal.close.then(function (result) {
                        });
                    });
                }
            }
            catch(e){
                
            }
        }

        function checkUpdateError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message','Unable to check for updates.','Close');
        }


        function activate() {
            getVersion();

            //get cpu info at 1 second intervals
            getPiInfo();
            $scope.timer = $interval(getPiInfo, 1000);

            getFanConfig();
            getButtonConfig();
        }

        $scope.$on("$destroy", function () {
            if (angular.isDefined($scope.timer)) {
                $interval.cancel($scope.timer);
            }
        });

        activate();
    }
})();