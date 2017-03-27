angular.module('piAdmin.common', ['ui.router', 'ui.bootstrap', 'LocalStorageModule', 'angularModalService', 'ionSlider']);
angular.module('piAdmin.auth', ['piAdmin.common']);
angular.module('piAdmin.alerts', ['piAdmin.common']);
angular.module('piAdmin.profile', ['piAdmin.common']);
angular.module('piAdmin.main', ['piAdmin.common']);
angular.module('piAdmin.dashboard', ['piAdmin.common']);
angular.module('piAdmin.games', ['piAdmin.common']);
angular.module('piAdmin.settings', ['piAdmin.common']);
angular.module('piAdmin.nfc', ['piAdmin.common']);

//app module
angular.module('piAdmin', ['piAdmin.common', 'piAdmin.auth', 'piAdmin.profile', 'piAdmin.main', 'piAdmin.dashboard', 'piAdmin.games', 'piAdmin.settings', 'piAdmin.nfc', 'piAdmin.alerts'])
    .config(function ($urlRouterProvider, $injector, $httpProvider) {
        // Register interceptors service
        $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
        $httpProvider.interceptors.push('authInterceptorService');

        $urlRouterProvider.otherwise(function ($injector) {
            var $state = $injector.get("$state");
            $state.go("main.dashboard");
        });
    })
    .controller('AppCtrl', ['$scope', '$rootScope', '$window', '$state', '$timeout', 'AppService', 'AlertService', 'ProfileService', function ($scope, $rootScope, $window, $state, $timeout, AppService, AlertService, ProfileService) {
        var vm = this;

        vm.pageName = 'Dashboard';

        vm.rebootPi = rebootPi;
        vm.shutdownPi = shutdownPi;
        vm.menuHide = menuHide;

        vm.showLoader = AppService.visibleLoader;

        function menuHide() {
            document.getElementById('navButton').click();
        }

        function rebootPi() {
            AlertService.alert('Reboot Pi', 'Are you sure you want to reboot the pi?','Reboot',initReboot,'Cancel');
            
            setTimeout(function () { window.location.href = window.location.href; }, 15000);
        }

        function initReboot(){
            AppService.rebootPi();
        }

        function shutdownPi() {
             AlertService.alert('Shutdown Pi', 'Are you sure you want to shutdown the pi?','Shutdown',initShutdown,'Cancel');            
        }

        function initShutdown(){
            AppService.shutdownPi();
        }

        function loadTheme() {
            ProfileService.getTheme().then(
                function (response) {
                    AppService.setTheme(response.data["theme"]);
                    AppService.activateTheme();
                },
                function (response) {
                    //
                }
            );
        }
        
        function activate() {
            $timeout(loadTheme,10);
        }

        activate();
    }])
    .directive('ngFileModel', ['$parse', function ($parse) {
        return {
            restrict: 'A',
            link: function (scope, element, attrs) {
                var model = $parse(attrs.ngFileModel);
                var isMultiple = attrs.multiple;
                var modelSetter = model.assign;
                element.bind('change', function () {
                    var values = [];
                    angular.forEach(element[0].files, function (item) {
                        values.push(item);
                    });
                    scope.$apply(function () {
                        if (isMultiple) {
                            modelSetter(scope, values);
                        } else {
                            modelSetter(scope, values[0]);
                        }
                    });
                });
            }
        };
    }])
    .run(['$rootScope', '$state', 'authService', 'AppService', function ($rootScope, $state, authService, AppService) {
        authService.fillAuthData();

        $rootScope.$on('$stateChangeStart', function (event, next) {
            if (next.name !== 'login') {
                pageName = next.name.toUpperCase().split(".");
                pageName = pageName[pageName.length-1];
                $rootScope.pageName = pageName;
                AppService.setPageName(pageName);
                if (!authService.authentication.isAuth) {
                    event.preventDefault();
                    $rootScope.redirectUrl = next.url;
                    $state.go("login");
                }
            }
        });
    }]);