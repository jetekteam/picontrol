(function () {
    'use strict';
    angular.module('piAdmin.auth')
    .config(function ($stateProvider) {
        $stateProvider
        .state('login', {
            url:'/login',
            views: {
                'main': {
                    templateUrl: 'static/assets/app/login/login.html',
                    controller: 'LoginController',
                    controllerAs: 'loginCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Control - Login',
                permissions: '*'
            }
        });
    });
})();