(function () {
    'use strict';
    angular.module('piAdmin.settings')
    .service("SettingsService", SettingsService);

    SettingsService.$inject = ['$http', '$q'];

    function SettingsService($http, $q) {
        var service = this;
        
        service.setFanConfig = function (config, successFunction, errorFunction) {
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/fan/update',
                data: config,
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.getFanConfig = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/fan',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.setButtonConfig = function (option, successFunction, errorFunction) {
            $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/button/update',
                data: {'option':option},
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.getButtonConfig = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/button',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.getVersion = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/version',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.checkUpdate = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/version/check',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
                successFunction(response);
            }, function (response) {
                errorFunction(response);
            });
        };

        service.update = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/settings/version/update',
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