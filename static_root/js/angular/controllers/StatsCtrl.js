/**
 * The main controller for the app. The controller:
 * - retrieves and persists the model via the todoStorage service
 * - exposes the model to the template and provides event handlers
 */
angular.module('dashboard')
    .controller('StatsCtrl',[ '$scope', 'StatsService', 'asyncScript', function ($scope, StatsService, asyncScript) {
        'use strict';

        asyncScript.load('raphael',function(){
        asyncScript.load('morris',function(){
            $scope.graphData = [];

            StatsService.getAreaChart().then(function(graphData){
                  $scope.graphData = graphData;
//                  console.log($scope.graphData);
                  Morris.Area ({
                            element: 'area-chart',
                            data: graphData,
                            xkey: 'date',
                            ykeys: ['click','exp','reach'],
                            labels: ['click','exp','reach'],
                            pointSize: 3,
                            hideHover: 'auto',
                            lineColors: [App.chartColors[0], App.chartColors[1], App.chartColors[3]]
                 });
             });
             console.log($scope.graphData);


            $scope.xkeys = 'date';
            $scope.ykeys = ['click','exp','reach'];
            $scope.labels = ['Click','Exp','Reach'];

        }); //script
        }); //script


    }]);