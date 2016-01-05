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
        $scope.elementsPerPage = 10;
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

            // search field filtering
            var searchField = $scope.searchfield;
            if(searchField.length > 0){
                // filter elements out who do not contain the string in the searchField
                current = current.filter(function(value){
                    return _.contains(value.title.toLowerCase(), searchField.toLowerCase());
                });
            }


            // uni filtering
            // check if uni filtering is even needed. If every checkbox is checked or unchecked no filtering is applied.
            var uniTmp = _.values($scope.unis);
            var allSame = true;
            for(var i=0; i < uniTmp.length - 1; i++){
                if (uniTmp[i] != uniTmp[i+1]){allSame = false; break;}
            }

            // if all values not same, filter
            if(!allSame){
                current = current.filter(function(value){
                    return $scope.unis[value.school_name];
                });
            }

            // apply filter
            $scope.current = current;
        }

        $scope.initUnis = function(){
            $scope.all.forEach(function(value, index, arr){
                $scope.unis[value.school_name] = true;
            });
        }


        // loading data
        $http({
            method: 'GET',
            url: "./data/courses.json",
            header : {'Content-Type' : 'application/json; charset=UTF-8'}
        }).success(function (result) {
            result =  _.values(result);//remove when lukas changes the data.json to an arraz
            $scope.all = result;
            $scope.initUnis();

            $scope.refreshFilter();


        }).error(function (data) {
            console.log("Request failed");
        });

    }]);