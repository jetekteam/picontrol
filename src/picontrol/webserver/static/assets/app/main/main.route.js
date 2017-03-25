(function () {
    'use strict';
    angular.module('piAdmin.main')
    .config(function ($stateProvider) {
        $stateProvider
        .state('main', {
            views: {
                'main': {
                    templateUrl: 'static/assets/app/main/main.html',
                    controller: 'MainController',
                    controllerAs: 'mainCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Control'
            }
        });
    });
})();