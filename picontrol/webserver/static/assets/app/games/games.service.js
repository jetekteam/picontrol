(function () {
    'use strict';
    angular.module('piAdmin.games')
    .service("GamesService", GamesService);

    GamesService.$inject = ['$http', '$q'];

    function GamesService($http, $q) {
        var service = this;

        service.selectedGame = {};

        service.setSelectedGame = function (selectedGame) {
            service.selectedGame = selectedGame;
        }

        service.getSelectedGame = function () {
            return service.selectedGame;
        }

        service.setSelectedConsole = function (selectedConsole){
            service.selectedConsole = selectedConsole;
        }

        service.getSelectedConsole = function (){
            return service.selectedConsole;
        }

        service.getConsoleList = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/game/consoles',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };
        
        service.getGameList = function (gameConsole, successFunction, errorFunction) {
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/game/games',
                dataType: 'json',
                data: gameConsole,
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.upload = function (gameConsole, files, successFunction, errorFunction, progressFunction) {
            var fd = new FormData();
            fd.append('console',JSON.stringify(gameConsole));
            fd.append('fileCount', files.length);
            for(var i = 0; i <= files.length-1; i++){
                fd.append('file_' + i,files[i]);
            }
            
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/game/upload',
                data: fd,
                headers: { "Content-Type": undefined }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.runGame = function (romString, successFunction, errorFunction) {
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/game/run',
                data: romString,
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.deleteGame = function (path, successFunction, errorFunction) {
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/game/delete',
                data: path,
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };
    }
})();