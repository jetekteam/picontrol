(function () {
    'use strict';
    angular.module('piAdmin.games')
    .config(function ($stateProvider) {
        $stateProvider
        .state('main.settings', {
            url: '/settings',
            views: {
                'app': {
                    templateUrl: 'static/assets/app/settings/settings.html',
                    controller: 'SettingsController',
                    controllerAs: 'settingsCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Amin - Settings'
            }
        });
    });
})();