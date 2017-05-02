(function () {
    'use strict';
    angular.module('piAdmin.profile')
    .config(function ($stateProvider) {
        $stateProvider
        .state('main.profile', {
            url: '/profile',
            views: {
                'app': {
                    templateUrl: 'static/assets/app/profile/profile.html',
                    controller: 'ProfileController',
                    controllerAs: 'profileCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Control - Profile'
            }
        });
    });
})();