(function () {
    'use strict';
    angular.module('piAdmin.games')
    .controller("GameModalController", GameModalController);

    GameModalController.$inject = ['$scope', '$rootScope', '$state', 'GamesService', 'NfcService', 'AlertService', 'AppService'];

    function GameModalController($scope, $rootScope, $state, GamesService, NfcService, AlertService, AppService) {
        var vm = this;

        vm.selectedGame = GamesService.getSelectedGame();

        vm.writeNfc = writeNfc;

        function writeNfc() {
            AppService.setLoaderVisible(true);
            var romString = JSON.stringify(vm.selectedGame.romString);
            NfcService.writeNfc(romString, writeNfcSuccess, writeNfcError);
        }

        function writeNfcSuccess(response) {
            AlertService.alert('Message', response.data.message, 'Close');
            AppService.setLoaderVisible(false);
        }

        function writeNfcError(response) {
            AppService.setLoaderVisible(false);
        }

        function activate() {
        }

        activate();
    }
})();