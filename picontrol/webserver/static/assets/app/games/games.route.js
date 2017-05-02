(function () {
    'use strict';
    angular.module('piAdmin.games')
    .config(function ($stateProvider) {
        $stateProvider
        .state('main.games', {
            url: '/games',
            views: {
                'app': {
                    templateUrl: 'static/assets/app/games/games.html',
                    controller: 'GamesController',
                    controllerAs: 'gamesCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Amin - Games'
            }
        });
    });
})();