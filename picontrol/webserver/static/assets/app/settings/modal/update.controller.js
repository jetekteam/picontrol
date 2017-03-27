(function () {
    'use strict';
    angular.module('piAdmin.settings')
    .controller("UpdateController", UpdateController);

    UpdateController.$inject = ['$scope', '$rootScope', '$state', '$window', '$location', 'AlertService', 'AppService', 'SettingsService'];

    function UpdateController($scope, $rootScope, $state, $window, $location, AlertService, AppService, SettingsService) {
        var vm = this;

        vm.update = update;

        function update() {
            AppService.setLoaderVisible(true);
            SettingsService.update(updateSuccess, updateError)
        }

        function updateSuccess(response) {
            AppService.setLoaderVisible(false);
            var updateInfo = response.data.update;
            if (updateInfo == false) {
                AlertService.alert('Message','Unable to update.','Close');
            }
            else{
                AlertService.alert('Message','Pi Control was updated to v' + updateInfo + ', please reboot for changes to take effect.','Close');
            }
        }

        function updateError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message','Unable to update.','Close');
        }
    }
})();