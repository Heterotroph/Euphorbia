function tracking(sUNIXTime, eUNIXTime) {

    //Длительность прелоадера
    var preloaderDelay = 30000;

    //Текущий ID сайта/пикселя
    var currentSPID = contentData.trackTreetableData[0]["spID"];
    //Текущий ключ по которому можно получить currentSPID
    var currentSPKey = getSPQueryKey(contentData.trackTreetableData[0]["id"]);
    //Имя текущего сайта/пикселя
    var currentName = contentData.trackTreetableData[0]["value"];


    //Старт вебикса
    webix.ready(function () {
        buildLeftMenu(menuData, "leftMenuContainerInner", leftMenuClick);
        $$("leftMenuID").select(1);

        contentData["viewLabelText"] = "Количество посещений " + "«" + currentName + "»";
        contentData["timeLabelText"] = "Средняя длительность посещений " + "«" + currentName + "»" + " (сек.)";
        buildContentTop(0, "contentContainerInnerTopWebix", refreshClick);
        buildContentBase(contentData, "contentContainerInner", treetableClick);
        $$("trackTreetableID").select(1);
    });

    //Добавляем календарь
    buildCalendar("#reportrange", dateClick, sUNIXTime, eUNIXTime)

    //Обработка нажатия на меню слева
    function leftMenuClick(itemID) {
        document.location.href = menuData.leftMenuLinks[itemID - 1]
    }

    //Обработка нажатия на выбор даты
    function dateClick(start, end) {
        sUNIXTime = end.unix();
        eUNIXTime = start.unix();
        if (end.diff(start.startOf('day'), "days") + 1 <= 60) {
            refreshClick();
        } else {
            webix.alert("Количество дней между датами должно быть не более 60.<br />Сократите диапазон.");
        }
    }

    //Обработка кнопки "обновить"
    function refreshClick() {
        loadRefresh(5);
        $$("trackTreetableID").showProgress({
            type: "bottom",
            delay: preloaderDelay,
            hide: false
        });

        $$("visitChartID").showProgress({
            type: "icon",
            delay: preloaderDelay
        });

        $$("timeChartID").showProgress({
            type: "icon",
            delay: preloaderDelay
        });
    }

    //Обработка выбора сайта из списка
    function treetableClick(itemID) {
        var spID = getSPIDByRow(itemID);
        if (spID) {
            if (spID != currentSPID) {
                loadSPData(getSPQueryKey(itemID), spID, 5)
                $$("trackTreetableID").showProgress({
                    type: "bottom",
                    delay: preloaderDelay,
                    hide: false
                });

                $$("visitChartID").showProgress({
                    type: "icon",
                    delay: preloaderDelay
                });

                $$("timeChartID").showProgress({
                    type: "icon",
                    delay: preloaderDelay
                });
            }
        }
    }

    //Получение ID сайта или страницы (пикселя) на основе ID в списке treetable
    function getSPIDByRow(value) {
        return spIDData[value];
    }

    //Получение site_id или page_id для query string
    function getSPQueryKey(value) {
        return ["site_id", "page_id"][Number(value.indexOf(".") != -1)];
    }

    //Загрузка данных для графиков-хуяфиков и тритейбла, по нажатию "обновить"
    function loadRefresh(attempts) {
        if (attempts <= 0) {
            $$("trackTreetableID").hideProgress();
            $$("visitChartID").hideProgress();
            $$("timeChartID").hideProgress();
            webix.alert("Упс.<br>Проверьте интернет соединение и нажмите «OK»", function (result) { location.reload(); });
            return;
        }
        var reqData = {};
        reqData["command"] = "get_refresh_data";
        reqData[currentSPKey] = currentSPID;
        reqData["to_date"] = eUNIXTime;
        reqData["from_date"] = sUNIXTime;
        $.ajax({
            url: "/platform/tracking_ajax/",
            type: "get",
            data: reqData,
            success: function (response) {
                spUpdate(response);
                ttUpdate(response);
                spIDData = response.spIDData
                $$("trackTreetableID").hideProgress();
                $$("visitChartID").hideProgress();
                $$("timeChartID").hideProgress();
            },
            error: function (xhr) {
                loadRefresh(attempts - 1)
            }
        });
    }

    //Загрузка данных для графиков-хуяфиков (Рекурсия)
    function loadSPData(spKey, spID, attempts) {
        if (attempts <= 0) {
            webix.alert("Упс.<br>Проверьте интернет соединение и нажмите «OK»", function (result) { location.reload(); });

            setVisibleWebixComponent("visitChartID", false);
            setVisibleWebixComponent("viewToolbarID", false);
            setVisibleWebixComponent("timeChartID", false);
            setVisibleWebixComponent("timeToolbarID", false);

            return;
        }
        var reqData = {};
        reqData["command"] = "get_data_by_sp_id";
        reqData[spKey] = spID;
        reqData["to_date"] = eUNIXTime;
        reqData["from_date"] = sUNIXTime;

        $.ajax({
            url: "/platform/tracking_ajax/",
            type: "get",
            data: reqData,
            success: function (response) {
                spUpdate(response);
                currentSPID = spID;
                currentSPKey = spKey
                $$("trackTreetableID").hideProgress();
                $$("visitChartID").hideProgress();
                $$("timeChartID").hideProgress();;
            },
            error: function (xhr) {
                loadSPData(spKey, spID, attempts - 1);
                $$("trackTreetableID").hideProgress();
                $$("visitChartID").hideProgress();
                $$("timeChartID").hideProgress();
            }
        });
    }

    //Вывод полученной инфы в гуй (графики-хуяфики)
    function spUpdate(dataJSON) {
        currentName = dataJSON.spName;

        var isVisible = dataJSON.visitChartData.length > 1;
        setVisibleWebixComponent("visitChartID", isVisible);
        setVisibleWebixComponent("viewToolbarID", isVisible);

        if (!isVisible) {
            webix.alert("Графики можно показать только при выборе двух и более дней...");
        }

        $$("visitChartID").clearAll();
        //$$("visitChartID").yAxis = dataJSON.visitChartYAxis;
        $$("visitChartID").parse(dataJSON.visitChartData)
        $$("visitChartID").refresh();
        $$("visitChartID").render();
        $$("viewToolbarLabelID").define("label", "Количество посещений " + "«" + currentName + "»");
        $$("viewToolbarLabelID").refresh();

        isVisible = dataJSON.timeChartData.length > 1;
        setVisibleWebixComponent("timeChartID", isVisible);
        setVisibleWebixComponent("timeToolbarID", isVisible);

        $$("timeChartID").clearAll();
        //$$("timeChartID").yAxis = dataJSON.timeChartYAxis;
        $$("timeChartID").parse(dataJSON.timeChartData);
        $$("timeChartID").refresh();
        $$("timeChartID").render();
        $$("timeToolbarLabelID").define("label", "Средняя длительность посещений " + "«" + currentName + "»" + " (сек.)");
        $$("timeToolbarLabelID").refresh();
    }

    //Вывод полученной инфы в гуй (тритейбл)
    function ttUpdate(dataJSON) {
        $$("trackTreetableID").parse(dataJSON.trackTreetableData);
    }

    //На кой хер эти господа из вебикс сделали методы show и hide? Лучше б что-нить типа visible...
    function setVisibleWebixComponent(compID, isVisible) {
        if (isVisible) {
            $$(compID).show();
        } else {
            $$(compID).hide();
        }
    }
}