angular.module('dashboard')
    .directive('areaChart',  function(){
        return {
            restrict: 'E',
            transclude: true,
            template: '<div id="area-chart"></div>',
            replace: true,
            link: function(scope, element, attrs){
                element.empty();
                element.addClass('chart-holder');
//                console.log(scope);


            }
        }
    });