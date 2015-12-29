'use strict';
function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

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
        $scope.currentLength = 0;
        $scope.searchfield = "";
        $scope.unis = [];

        $scope.maxBackgroundImages = 5;
        $scope.backgroundId = getRandomInt(1, $scope.maxBackgroundImages + 1);

        $scope.searchFieldChange = function() {
          if($scope.searchfield.length == 0){
            $scope.current = $scope.all;
            $scope.currentLength = 1;
          }

          $scope.current = {};
          $scope.currentLength = 0;
          var data = $scope.all;
          for (var key in data) {
            if (data[key].title.toLowerCase().indexOf($scope.searchfield.toLowerCase()) > -1) {
              $scope.current[key] = data[key];
              $scope.currentLength += 1;
            }
          }
          console.log($scope.current);
        }

        $scope.initUnis = function(){
            var data = $scope.all;
            var unis = {}
            for (var key in $scope.all) {
                var uni = data[key]['school_name'];
                unis[uni] = uni;
            }

            $scope.unis = Object.keys(unis);
        }


        // loading data
        $http({
            method: 'GET',
            url: "./data/courses.json",
            header : {'Content-Type' : 'application/json; charset=UTF-8'}
        }).success(function (result) {
            $scope.all = result;
            $scope.current = result;

            $scope.initUnis();
        }).error(function (data) {
            console.log("Request failed");
        });

    }]);