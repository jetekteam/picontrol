(function () {
    'use strict';
    angular.module('piAdmin.nfc')
    .controller("NfcController", NfcController);

    NfcController.$inject = ['$scope', '$rootScope', '$state', '$window', '$location', 'NfcService', 'ModalService', 'AlertService', 'AppService'];

    function NfcController($scope, $rootScope, $state, $window, $location, NfcService, ModalService, AlertService, AppService) {
        var vm = this;

        vm.nfcTag = {console:'', rom:''}

        vm.readTag = readTag;
        vm.writeTag = writeTag;
        vm.clear = clear;

        function readTag() {
            AppService.setLoaderVisible(true);
            NfcService.readNfc(readTagSuccess, readTagError);
        }

        function readTagSuccess(response) {
            AppService.setLoaderVisible(false);
            if (response.data.type == 'success'){
                var message = response.data.data;
                if (message.records[0]) {
                    vm.nfcTag.console = message.records[0];
                }
                if (message.records[1]) {
                    vm.nfcTag.rom = message.records[1];
                }
            }
            else{
                AlertService.alert('Error', response.data.message,'Close');
                vm.nfcTag.console = '';
                vm.nfcTag.rom = '';
            }
        }

        function readTagError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Error','An error occured while trying to read the NFC Tag, unable to find NFC device.','Close');
        }

        function writeTag(){
            AppService.setLoaderVisible(true);
            var tagInfo = { console: vm.nfcTag.console, rom: vm.nfcTag.rom };
            var tagString = JSON.stringify(tagInfo);
            NfcService.writeNfc(tagString,writeTagSuccess,writeTagError);
        }

        function writeTagSuccess(response) {
            AppService.setLoaderVisible(false);
            if (response.data.type == 'success'){
                AlertService.alert('Successfull', response.data.message,'Close');
            }
            else{
                AlertService.alert('Error', response.data.message,'Close');
            }
        }

        function writeTagError(response) {
            AppService.setLoaderVisible(false);
            AlertService.alert('Error','An error occured while trying to write the NFC Tag.','Close');
        }

        function clear() {
            vm.nfcTag.console = '';
            vm.nfcTag.rom = '';
        }

        function activate() {
        }

        activate();
    }
})();