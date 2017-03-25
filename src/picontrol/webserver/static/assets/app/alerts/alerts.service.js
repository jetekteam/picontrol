(function () {
    'use strict';
    angular.module('piAdmin.alerts')
    .service("AlertService", AlertService);

    AlertService.$inject = ['$rootScope', 'ModalService'];

    function AlertService($rootScope, ModalService) {
        var service = this;

        service.alert = function(headerText, bodyText, buttonText, method, buttonText2){

            method = method || function(){};
            buttonText2 = buttonText2 || '';

            var scope = $rootScope.$new();
            scope.headerText = headerText;
            scope.bodyText = bodyText;
            scope.buttonText = buttonText;
            scope.method = method;
            scope.buttonText2 = buttonText2;

            var modalInstance = ModalService.showModal({
                scope: scope,
                templateUrl: 'static/assets/app/alerts/alerts_modal.html',
                controller: 'AlertModalCtroller'
            }).then(function (modal) {
                modal.element.modal();
                modal.close.then(function (result) {
                });
            });
        }
    }
})();