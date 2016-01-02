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
        $scope.unis = {};

        $scope.maxBackgroundImages = 5;
        $scope.backgroundId = getRandomInt(1, $scope.maxBackgroundImages + 1);

        $scope.toggleUni = function(uni){
            $scope.unis[uni] = !$scope.unis[uni];
            $scope.refreshFilter();
        }

        $scope.searchFieldChange = function() {
            $scope.refreshFilter();
        }

        $scope.refreshFilter = function(){
            var current = $scope.all;
            var tmp = {};

            // search field filtering
            var searchField = $scope.searchfield;
            if(searchField.length > 0){
                for (var key in current) {
                    if (current[key].title.toLowerCase().indexOf(searchField.toLowerCase()) > -1) {
                        tmp[key] = current[key];
                    }
                }
                current = tmp;
            }


            // uni filtering
            // check if uni filtering is even needed. If every checkbox is checked or unchecked no filtering is applied.
            var uniTmp = Object.keys($scope.unis).map(function(key){return $scope.unis[key];});
            var allSame = true;
            for(var i=0; i < uniTmp.length - 1; i++){
                if (uniTmp[i] != uniTmp[i+1]){allSame = false; break;}
            }

            // if all values not same, filter
            if(!allSame){
                var selected = Object.keys($scope.unis).filter(function(v){return $scope.unis[v]});
                var tmp = {}
                for (var key in current) {
                    if (selected.indexOf(current[key].school_name) > -1) {
                        tmp[key] = current[key];
                    }
                }
                current = tmp;
            }

            // apply filter
            $scope.current = current;
        }

        $scope.initUnis = function(){
            for (var key in $scope.all) {
                var uni = $scope.all[key]['school_name'];
                $scope.unis[uni] = true;
            }
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