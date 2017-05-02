(function () {
    'use strict';
    angular.module('piAdmin')
    .service("AppService", AppService);

    AppService.$inject = ['$http', '$q'];

    function AppService($http, $q) {
        var service = this;

        service.visibleLoader = [];

        service.pageName = '';
        service.theme = 'default';

        service.setPageName = function (value) {
            service.pageName = value;
        }

        service.getPageName = function () {
            return service.pageName;
        }

        service.setLoaderVisible = function (value) {
            if (service.visibleLoader.length == 0 && value){
                service.visibleLoader.push('true');
            }
            else {
                if (service.visibleLoader.length > 0) {
                    service.visibleLoader.splice(0,1);
                }
            }
        }

        service.getTheme = function () {
            return service.theme;
        }

        service.setTheme = function (theme) {
            service.theme = theme;
        }

        service.activateTheme = function () {
             $(".app").removeClass("app-default");
             $(".app").removeClass("app-green");
             $(".app").removeClass("app-blue");
             $(".app").removeClass("app-blue-sky");
             $(".app").removeClass("app-yellow");
             $(".app").removeClass("app-red");
             $(".app").addClass("app-" + service.theme);      
        }

        service.shutdownPi = function () {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/shutdown',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
            }, function (response) {
            });
        };

        service.rebootPi = function () {
            $http({
                method: "GET",
                async: true,
                crossDomain: true,
                url: '../api/pi/reboot',
                dataType: 'json',
                headers: { "Content-Type": "application/json" }
            }).then(function (response) {
            }, function (response) {
            });
        };
    }
})();