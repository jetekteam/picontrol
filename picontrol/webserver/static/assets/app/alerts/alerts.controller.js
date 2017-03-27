(function () {
    'use strict';
    angular.module('piAdmin.alerts')
    .controller("AlertModalCtroller", AlertModalCtroller);

    AlertModalCtroller.$inject = ['$scope'];

    function AlertModalCtroller($scope) {
        var service = this;

        $scope.ok = function () {
            if ($scope.method) {
                $scope.method();
            }
            //$uibModalInstance.dismiss('cancel');
        };

        $scope.cancel = function () {
            //$uibModalInstance.dismiss('cancel');
        };
    }
})();