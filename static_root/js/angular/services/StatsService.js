/**
 * Services that persists and retrieves TODOs from localStorage
 */
angular.module('dashboard')
    .factory('StatsService', function ($http) {
        'use strict';
        return {
            getAreaChart: function(){
                return $http.get('http://localhost:8000/api/campain/').then(function(response){
//                    console.log(response);
                    return response.data.data.entry.content.statUniqueObject.stat.item;
                })
            }
        }


    }).
    service('asyncScript', ['$window', function($window) {

        /* on-demand async script loader using jQuery getScript */

        // central config for dependencies - manage libs and versions here..
        var libs = {

            flot:        '//cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.min.js',
            flot_resize: 'http://www.flotcharts.org/flot/jquery.flot.resize.js',
            flot_pie:    '//cdnjs.cloudflare.com/ajax/libs/flot/0.8.2/jquery.flot.pie.min.js',
            raphael:     '//cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js',
            morris:      '//cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.0/morris.min.js',
            hotkeys:     'http://mindmup.github.io/bootstrap-wysiwyg/external/jquery.hotkeys.js',
            wysiwyg:     'http://mindmup.github.io/bootstrap-wysiwyg/bootstrap-wysiwyg.js',
            datepicker:  '//cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.3.0/js/bootstrap-datepicker.min.js',
            moment:      '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.6.0/moment.min.js',
            bootstrapdatetimepicker:'//cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/3.0.0/js/bootstrap-datetimepicker.min.js',
            jasny:       '//cdnjs.cloudflare.com/ajax/libs/jasny-bootstrap/3.1.3/js/jasny-bootstrap.min.js',
            jvectormap:  'http://jvectormap.com/js/jquery-jvectormap-1.2.2.min.js',
            jvectormap_en:'http://jvectormap.com/js/jquery-jvectormap-world-mill-en.js',
            dropzone:    '//cdnjs.cloudflare.com/ajax/libs/dropzone/3.8.4/dropzone.min.js',
            minicolors:  '//cdn.jsdelivr.net/jquery.minicolors/2.1.2/jquery.minicolors.js',
            starr:       '/lib/starrr.js',
            selectpicker:'//cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.5.4/bootstrap-select.min.js',
            fullcalandar:'//cdnjs.cloudflare.com/ajax/libs/fullcalendar/1.6.4/fullcalendar.min.js',
            gcal:        '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/1.6.4/gcal.js',
            angular_calendar:'//cdnjs.cloudflare.com/ajax/libs/angular-ui-calendar/0.8.0/calendar.min.js'

        };

        return {

            load: function(name,cb) {

                /* async load if not already attached to $window */
                if (!$window["loader_"+name]) {
                    // load it
                    $.getScript(libs[name],function(){
                        $window["loader_"+name] = true;
                        cb();
                    });
                }
                else {
                    // script is already available to window - do callback
                    cb();
                }
            }
        }

    }]);