(function () {
    'use strict';
    angular.module('piAdmin.profile')
    .service("ProfileService", ProfileService);

    ProfileService.$inject = ['$http', '$q'];

    function ProfileService($http, $q) {
        var service = this;

        service.setUser = function (user) {
            return $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/profile/user/update',
                data: user,
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            });
        };

        service.getUser = function () {
            return $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/profile/user',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            });
        };

        service.setTheme = function (theme) {
            return $http({
                method: "POST",
                async: true,
                crossDomain: true,
                url: '../api/profile/theme/update',
                data: {'theme':theme},
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            });
        };

        service.getTheme = function () {
            return $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/profile/theme',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            });
        };
    }
})();