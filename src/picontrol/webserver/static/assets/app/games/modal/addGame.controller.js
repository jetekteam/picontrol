(function () {
    'use strict';
    angular.module('piAdmin.games')
    .controller("AddGameController", AddGameController);

    AddGameController.$inject = ['$scope', '$rootScope', '$state', 'GamesService', 'AlertService', 'AppService'];

    function AddGameController($scope, $rootScope, $state, GamesService, AlertService, AppService) {
        var vm = this;

        vm.selectedConsole = {};
        vm.files = [];

        vm.setSelectedConsole = setSelectedConsole;
        vm.upload = upload;

        function setSelectedConsole(console) {
            vm.selectedConsole = console;
            
        }

        function getConsoleList() {
            GamesService.getConsoleList(getConsoleListSuccess, getConsoleListError);
        }

        function getConsoleListSuccess(response) {
            vm.consoles = response.data;

            for (var i = 0; i <= vm.consoles.length-1; i++){
                if (vm.consoles[i].name == GamesService.getSelectedConsole().name){
                    setSelectedConsole(vm.consoles[i]);
                    break;
                }
            }

           // vm.setSelectedConsole(vm.consoles[0]);
        }

        function getConsoleListError(response) {

        }

        function upload() {
            AppService.setLoaderVisible(true);
            GamesService.upload(vm.selectedConsole, vm.files, uploadSuccess, uploadError);
        }

        function uploadSuccess(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Message', response.data.message, 'Close');
            $rootScope.$broadcast('reloadConsoles');
        }

        function uploadError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Error', 'Upload failed.', 'Close');
        }
        
        function activate() {
            getConsoleList();
        }

        activate();
    }
})();