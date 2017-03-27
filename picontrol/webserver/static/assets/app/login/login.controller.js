(function () {
    'use strict';
    angular.module('piAdmin.auth')
    .controller('LoginController', LoginController);

    LoginController.$inject = ['$scope', '$rootScope', '$location', 'authService', 'AppService', 'ProfileService'];

    function LoginController($scope, $rootScope, $location, authService, AppService, ProfileService) {
        var vm = this;

        vm.loginData = {
            userName: "",
            password: ""
        };

        vm.button = 'success';
 
        vm.alerts = [];
 
        vm.login = function () {
            vm.alerts = [];
            authService.login(vm.loginData).then(function (response) {
                if ($rootScope.redirectUrl) {
                    $location.path($rootScope.redirectUrl);
                }
                else {
                    $location.path('/dashboard');
                }
            },
            function (err) {
                vm.alerts.push({'message':'Invalid Credentials.', 'type':'warning'});
            });
        };

        function activate() {
            AppService.activateTheme();
            var theme = AppService.getTheme();
            switch(theme){
                case 'green':
                    vm.button = 'success';
                    break;
                case 'blue':
                    vm.button = 'info';
                    break;
                case 'blue-sky':
                    vm.button = 'info';
                    break;
                case 'yellow':
                    vm.button = 'warning';
                    break;
                case 'red':
                    vm.button = 'danger';
                    break;
                default:
                    vm.button = 'success';
                    break;
            }
        }

        activate();

    }
})();