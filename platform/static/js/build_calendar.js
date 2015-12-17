function buildCalendar(container, dateCallback, sUNIXTime, eUNIXTime) {

    function cb(start, end) {
        $(container + ' span').html(start.format('DD.MM.YY') + ' - ' + end.format('DD.MM.YY'));
        dateCallback(start, end);
    }

    $(container).daterangepicker({
        locale: {
            "format": "DD.MM.YYYY",
            "separator": " - ",
            "applyLabel": "Применить",
            "cancelLabel": "Отмена",
            "fromLabel": "С",
            "toLabel": "по",
            "customRangeLabel": "Выбрать диапазон",
            "daysOfWeek": [
                "вс",
                "пн",
                "вт",
                "ср",
                "чт",
                "пт",
                "сб"
            ],
            "monthNames": [
                "Январь",
                "Февраль",
                "Март",
                "Апрель",
                "Май",
                "Июнь",
                "Июль",
                "Август",
                "Сентябрь",
                "Октябрь",
                "Ноябрь",
                "Декабрь"
            ],
            "firstDay": 1
        },
        ranges: {
            'Сегодня': [moment(), moment()],
            'Вчера': [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
            'Последние 7 дней': [moment().subtract(6, 'days'), moment()],
            'Последние 30 дней': [moment().subtract(29, 'days'), moment()],
            'Текущий месяц': [moment().startOf('month'), moment()],
            'Предыдущий месяц': [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
        },
        linkedCalendars: true,
        startDate: moment(sUNIXTime),
        endDate: moment(eUNIXTime),
        opens: "right",
        isInvalidDate: function(value){
            return value > moment() || value < moment().subtract(12, 'month');
        }
    }, cb);

    $(container + ' span').html(moment(sUNIXTime).format('DD.MM.YY') + ' - ' + moment(eUNIXTime).format('DD.MM.YY'));
}