(function () {
    'use strict';
    angular.module('piAdmin.dashboard')
    .config(function ($stateProvider) {
        $stateProvider
        .state('main.dashboard', {
            url: '/dashboard',
            views: {
                'app': {
                    templateUrl: 'static/assets/app/dashboard/dashboard.html',
                    controller: 'DashboardController',
                    controllerAs: 'dashboardCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Amin - Dashboard'
            }
        });
    });
})();