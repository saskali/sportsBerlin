'use strict';

angular.module('myApp.view1', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$http', '$scope', function ($http, $scope) {
        $scope.data = null;

        // loading data
        $http({
            method: 'GET',
            url: "./data/courses.json"
        }).success(function (result) {
            $scope.data = result;
        }).error(function (data) {
            console.log("Request failed");
        });

    }]);