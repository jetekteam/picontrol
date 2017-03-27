(function () {
    'use strict';
    angular.module('piAdmin.games')
    .controller("GamesController", GamesController);

    GamesController.$inject = ['$scope', '$rootScope', '$state', '$window', '$location', 'GamesService', 'AppService', 'ModalService', 'AlertService'];

    function GamesController($scope, $rootScope, $state, $window, $location, GamesService, AppService, ModalService, AlertService) {
        var vm = this;

        vm.listType = 'grid';
        vm.selectedConsole = null;
        vm.consoles = []

        vm.grid = {header:[],rows:[]};
        vm.gameList = [];

        vm.setSelectedConsole = setSelectedConsole;
        vm.runGame = runGame;
        vm.writeNfc = writeNfc;
        vm.addGames = addGames;
        vm.deleteGame = deleteGame;

        $scope.$on('reloadConsoles', function (event, args) {
            getConsoleList();
        });

        function setSelectedConsole(console) {
            vm.selectedConsole = console;
            GamesService.setSelectedConsole(console);
            getGameList();
        }

        function getGameList() {
            GamesService.getGameList(vm.selectedConsole, getGameListSuccess, getGameListError);
        }

        function getGameListSuccess(response) {
            vm.gameList = response.data.games;
            vm.grid.rows = vm.gameList;

            setTimeout(function (){$('[data-toggle="tooltip"]').tooltip(); },100);
        }

        function getGameListError(response) {

        }

        function getConsoleList() {
            GamesService.getConsoleList(getConsoleListSuccess, getConsoleListError);
        }

        function getConsoleListSuccess(response) {
            vm.consoles = response.data;
            var existsInList = false;
            for (var i = vm.consoles.length - 1; i > -1; i--) {
                if (vm.consoles[i].fileCount == 0) {
                    vm.consoles.splice(i,1);
                }
                else{
                    if (vm.selectedConsole) {
                        if (vm.consoles[i]['name'] == vm.selectedConsole['name']) {
                            existsInList = true;
                        }
                    }
                }
            }

            if (!existsInList){
                vm.setSelectedConsole(vm.consoles[0]);
            }
            getGameList();
        }

        function getConsoleListError(response) {

        }

        function writeNfc(game) {
            GamesService.setSelectedGame(game);
            ModalService.showModal({
                templateUrl: 'static/assets/app/games/modal/game.html',
                controller: 'GameModalController',
                controllerAs: 'gameModalCtrl'
            }).then(function (modal) {
                modal.element.modal();
                modal.close.then(function (result) {
                });
            });
        }

        function addGames() {
            GamesService.setSelectedConsole(vm.selectedConsole);
            ModalService.showModal({
                templateUrl: 'static/assets/app/games/modal/addGame.html',
                controller: 'AddGameController',
                controllerAs: 'addGameCtrl'
            }).then(function (modal) {
                modal.element.modal();
                modal.close.then(function (result) {
                });
            });
        }

        function runGame(game) {
            AppService.setLoaderVisible(true);
            GamesService.runGame(game.romString, runGameSuccess, runGameError);
        }

        function runGameSuccess(response) {
            AppService.setLoaderVisible(false);
            if (response.data) {
                AlertService.alert('Game Started', 'Game started successfully.', 'Close');
            }
            else {
                //alert('Failed to start game');
            }
        }

        function runGameError(response) {
            AppService.setLoaderVisible(true);
        }

        function deleteGame(game){
            AlertService.alert('Delete Game', "Are you sure you want to delete '" + game.name + "'?", "Delete", function () {deleteGameQ(game)}, 'Cancel');
        }

        function deleteGameQ(game) {
            AppService.setLoaderVisible(true);
            GamesService.deleteGame(game.path, deleteGameSuccess, deleteGameError)
        }

        function deleteGameSuccess(response){
            AppService.setLoaderVisible(false);
            getConsoleList();
        }

        function deleteGameError(response){
            AppService.setLoaderVisible(false);
        }

        function activate() {
            vm.grid.header = ["", "Game", "Play Count", "Description"];
            getConsoleList();

           
        }

        activate();
    }
})();