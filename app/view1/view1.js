'use strict';

angular.module('myApp.view1', ['ngRoute'])
    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/view1', {
            templateUrl: 'view1/view1.html',
            controller: 'View1Ctrl'
        });
    }])

    .controller('View1Ctrl', ['$http', '$scope', function ($http, $scope) {
        $scope.all = {};
        $scope.current = {};
        $scope.searchfield = "";

        $scope.searchFieldChange = function() {
          if($scope.searchfield.length == 0){
            $scope.current = $scope.all;
          }

          $scope.current = {};
          var data = $scope.all;
          for (var key in data) {
            if (data[key].title.toLowerCase().indexOf($scope.searchfield.toLowerCase()) > -1) {
              $scope.current[key] = data[key];
            }
          }
          console.log($scope.current);
        }

        // loading data
        $http({
            method: 'GET',
            url: "./data/courses.json",
            header : {'Content-Type' : 'application/json; charset=UTF-8'}
        }).success(function (result) {
            $scope.all = result;
            $scope.current = result;
        }).error(function (data) {
            console.log("Request failed");
        });

    }]);