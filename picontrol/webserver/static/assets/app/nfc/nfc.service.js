(function () {
    'use strict';
    angular.module('piAdmin.nfc')
    .service("NfcService", NfcService);

    NfcService.$inject = ['$http', '$q'];

    function NfcService($http, $q) {
        var service = this;

        service.writeNfc = function (tag, successFunction, errorFunction) {
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/nfc/write',
                data: tag,
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.readNfc = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/nfc/read',
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