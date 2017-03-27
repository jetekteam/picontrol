(function () {
    'use strict';
    angular.module('piAdmin.dashboard')
    .service("DashboardService", DashboardService);

    DashboardService.$inject = ['$http', '$q', 'authService'];

    function DashboardService($http, $q, authService) {
        var service = this;
        service.getPiInfo = function (successFunction, errorFunction) {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/info',
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