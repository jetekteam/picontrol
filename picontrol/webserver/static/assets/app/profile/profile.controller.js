(function () {
    'use strict';
    angular.module('piAdmin.profile')
    .controller("ProfileController", ProfileController);

    ProfileController.$inject = ['$scope', '$rootScope', '$state', 'AlertService', 'AppService', 'ProfileService'];

    function ProfileController($scope, $rootScope, $state, AlertService, AppService, ProfileService) {
        var vm = this;

        vm.user = {username:'',password:''}

        vm.theme = 'default';

        vm.saveUser = saveUser;
        vm.saveTheme = saveTheme;
        vm.setTheme = setTheme;

        function setTheme(value) {
            AppService.setTheme(value);
            AppService.activateTheme();
        }

        function getUser() {
            ProfileService.getUser(vm.user).then(
                function (response) {
                    vm.user = response.data;
                },
                function (response){
                    //do nothing
                }
            );
        }

        function saveUser() {
            ProfileService.setUser(vm.user).then(
                function (response) {
                    if (response.data) {
                        AlertService.alert('Message','User saved successfully.','Close');
                    }
                },
                function (response){
                    AlertService.alert('Error','Unable to save User.','Close');
                }
            );
        }

        function saveTheme() {
            ProfileService.setTheme(AppService.getTheme()).then(
                function (response) {
                    if (response.data) {
                        AlertService.alert('Message','Theme saved successfully.','Close');
                    }
                },
                function (response){
                    AlertService.alert('Error','Unable to save Theme.','Close');
                }
            );
        }
        
        function activate() { 
            vm.theme = AppService.getTheme();
            AppService.activateTheme();            
        }

        activate();
    }
})();