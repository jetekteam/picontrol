(function () {
    'use strict';
    angular.module('piAdmin.auth')
    .factory('authService', ['$http', '$q', 'localStorageService', function ($http, $q, localStorageService) {
 
        var serviceBase = location.origin + '/';
        var authServiceFactory = {};
 
        var _authentication = {
            isAuth: false,
            userName : ""
        };
        
        var _savePasswordChange = function (changePasswordData) {
        	try {
        		return $http.post(serviceBase + 'api/account/changepassword', changePasswordData)
                    .then(function (response) {
                    	return response;
                    }
                );
        	} catch (e) {
        		return e.message;
        	}
        }

        var _login = function (loginData) {
 
            var data = "username=" + loginData.userName + "&password=" + loginData.password;
 
            var deferred = $q.defer();
 
            $http.post(serviceBase + 'token', data, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }).success(function (response) {
                localStorageService.set('authorizationData', { token: response.access_token, userName: loginData.userName });
 
                _authentication.isAuth = true;
                _authentication.userName = loginData.userName;
 
                deferred.resolve(response);
 
            }).error(function (err, status) {
                _logOut();
                deferred.reject(err);
            });
 
            return deferred.promise;
 
        };
 
        var _logOut = function () {
 
            localStorageService.remove('authorizationData');
 
            _authentication.isAuth = false;
            _authentication.userName = "";
        };
 
        var _fillAuthData = function () {
            var authData = localStorageService.get('authorizationData');
            if (authData)
            {
                _authentication.isAuth = true;
                _authentication.userName = authData.userName;
            }
        }
 
        authServiceFactory.savePasswordChange = _savePasswordChange;
        authServiceFactory.login = _login;
        authServiceFactory.logOut = _logOut;
        authServiceFactory.fillAuthData = _fillAuthData;
        authServiceFactory.authentication = _authentication;
 
        return authServiceFactory;
    }]);
})();