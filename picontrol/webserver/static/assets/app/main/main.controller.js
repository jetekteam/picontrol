(function () {
    'use strict';
    angular.module('piAdmin.main')
    .controller('MainController', MainController);

    MainController.$inject = ['$scope', '$rootScope', '$location', 'authService', 'AppService', 'AlertService', 'ModalService', 'SettingsService'];

    function MainController($scope, $rootScope, $location, authService, AppService, AlertService, ModalService, SettingsService) {
        var vm = this;

        vm.getPageName = getPageName;
        vm.logout = logout;
        vm.shutdownPi = shutdownPi;
        vm.rebootPi = rebootPi;
        vm.openAccountSettings = openAccountSettings;

        function getPageName() {
            return AppService.getPageName();
        }

        function rebootPi() {
            AlertService.alert('Reboot Pi', 'Are you sure you want to reboot the PI?','Reboot',initReboot,'Cancel');
            
            setTimeout(function () { window.location.href = window.location.href; }, 15000);
        }

        function initReboot(){
            AppService.rebootPi();
        }

        function shutdownPi() {
             AlertService.alert('Shutdown Pi', 'Are you sure you want to shutdown the PI?','Shutdown',initShutdown,'Cancel');            
        }

        function initShutdown(){
            AppService.shutdownPi();
        }

        function logout() {
            authService.logOut();
            $location.path('/login');
        }

        function openAccountSettings() {
            ModalService.showModal({
                templateUrl: 'static/assets/app/account/account.html',
                controller: 'AccountController',
                controllerAs: 'accountCtrl'
            }).then(function (modal) {
                modal.element.modal();
                modal.close.then(function (result) {
                });
            });
        }

        function getVersion() {
            SettingsService.getVersion(getVersionSuccess, getVersion);
        }

        function getVersionSuccess(response) {
            vm.version = response.data;
        }

        function getVersionError(response) {

        }

        function activate() {
            AppService.activateTheme();
            getVersion();
        }

        activate();
    }
})();