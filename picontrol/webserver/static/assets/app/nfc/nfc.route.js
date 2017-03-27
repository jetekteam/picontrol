(function () {
    'use strict';
    angular.module('piAdmin.nfc')
    .config(function ($stateProvider) {
        $stateProvider
        .state('main.nfc', {
            url: '/nfc',
            views: {
                'app': {
                    templateUrl: 'static/assets/app/nfc/nfc.html',
                    controller: 'NfcController',
                    controllerAs: 'nfcCtrl'
                }
            },
            data: {
                pageTitle: 'Pi Control - NFC'
            }
        });
    });
})();