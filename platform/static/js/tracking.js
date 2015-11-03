function buildContent(data, containerID, dateCallback, refreshCallback, treetableCallback) {

	//  Тулбар
	var dtToolbar = {
		view: "toolbar",
		id: "dtToolbarID",
		width: 880,
		css: "webix-ui-dttoolbar",
		cols: [{},/*{
			view: "combo",
			id: "dtCombo",
			label: "Период",
			value: "Сегодня",
			yCount: "5",
			width: 200,
			options: data.toolbarDates
		},{}, {
			view: "button",
			type: "iconButton",
			icon: "edit",
			label: "Правка",
			width: 110,
			align: "right",
			click: function() {alert()}
		}, {
			view: "button",
			type: "iconButton",
			icon: "plus",
			label: "Добавить сайт",
			width: 165,
			align: "right",
			click: function() {alert()}
		},{
			view: "button",
			type: "iconButton",
			icon: "plus",
			label: "Добавить трекинг",
			width: 190,
			align: "right",
			click: function() {alert()}
		}, */{
			view: "button",
			type: "iconButton",
			icon: "refresh",
			label: "Обновить",
			width: 120,
			align: "right",
			click: refreshCallback
		}]

	}

	//  Таблица трекинга
	var trackTreetable = {
		view: "treetable",
		id: "trackTreetableID",
		width: 880,
		autoheight: true,
		minHeight: 150,
		select: "row",
		hover: "datatable_hover",
		scroll: false,
		tooltip:true,
		columns: [{
			id: "id",
			header: "",
			width: 50,
			css: "datatable_left_alignment"
		}, {
			id: "name",
			header: "Площадка",
			template: "{common.treetable()} #value#",
			fillspace: true,
		}, {
			id: "time",
			header:[{text: "Длительность посещений (медиана)", colspan:2, css:"datatable_rowspan_header"},{text:"Общая", css:"datatable_center_alignment" }],
			fillspace: 0.4,
			css: "datatable_center_alignment",
			tooltip:"Длительность среднестат. посещения более #time#"
		}, {
			id: "active",
			header:[null, {text:"Активная", css:"datatable_center_alignment" }],
			fillspace: 0.4,
			css: "datatable_center_alignment",
			tooltip:"Длительность активных действий посетителей более #active#"
		}, {
			id: "visits",
			header:[{text: "Количество посещений", colspan:2, css:"datatable_rowspan_header"},{text:"Всего", css:"datatable_center_alignment" }],
			css: "datatable_right_alignment"
		}, {
			id: "uniq",
			header:[null, {text:"Уникальные", css:"datatable_center_alignment" }],
			adjust: "header",
			css: "datatable_right_alignment"
		}],
		on:{
			"onItemClick":function(id, e, trg){
				treetableCallback(id.row);
			}
		},
		data: data.trackTreetableData
	};

	//График посещений
	var visitChart = {
		view: "chart",
		id: "visitChartID",
		type: "area",
		width: 880,
		height: 300,
		alpha: 0.7,
		scale: "linear",
		offset: false,
		//preset: "simple",
		xAxis: {
			template: "#xAxis#"
		},
		yAxis: {
			template:function(obj){return (obj)},
			origin: 0
		},
		//yAxis: data.visitChartYAxis,
		legend: {
			values: data.visitChartLegendData,
			valign: "top",
			align: "left",
			layout: "x"
		},
		eventRadius: 5,
		series: [{
			type: "area",
			value: "#views#",
			color: "#a7ee70",
			tooltip: {
				template: "#views# просм."
			}
		}, {
			type: "line",
			value: "#views#",
			color: "#a7ee70",
			tooltip: {
				template: "#views# просм."
			}
		}, {
			type: "area",
			value: "#reqs#",
			color: "#36abee",
			tooltip: {
				template: "#reqs# чел."
			}
		}, {
			type: "line",
			value: "#reqs#",
			color: "#36abee",
			tooltip: {
				template: "#reqs# чел."
			}
		}],
		data: data.visitChartData
	}

	//График времени
	var timeChart = {
		view: "chart",
		id: "timeChartID",
		type: "area",
		width: 880,
		height: 300,
		alpha: 0.7,
		scale: "linear",
		xAxis: {
			template: "#xAxis#"
		},
		yAxis: {
			template:function(obj){return (obj)},
			origin: 0
		},
		//yAxis: data.timeChartYAxis,
		legend: {
			values: data.timeChartLegendData,
			valign: "top",
			align: "left",
			layout: "x"
		},
		eventRadius: 5,
		series: [{
			type: "area",
			value: "#total#",
			color: "#a7ee70",
			tooltip: {
				template: "#total# сек."
			}
		}, {
			type: "line",
			value: "#total#",
			color: "#a7ee70",
			tooltip: {
				template: "#total# сек."
			}
		}, {
			type: "area",
			value: "#active#",
			color: "#36abee",
			tooltip: {
				template: "#active# сек."
			}
		}, {
			type: "line",
			value: "#active#",
			color: "#36abee",
			tooltip: {
				template: "#active# сек."
			}
		}],
		data: data.timeChartData
	}

	var editWindow = {
    	view:"window",
   		id:"editWindow",
   		head:"Правка",
    	body:{
    	}
	}

	var createSiteWindow = {
    	view:"window",
   		id:"createSiteWindow",
   		head:"Добавить сайт",
    	body:{
    	}
	}

	var createTrackingWindow = {
    	view:"window",
   		id:"createTrackingWindow",
   		head:"Добавить трекинг на страницу",
    	body:{
    	}
	}

	webix.ui({
		css: "wbx",
		container: containerID,
		rows: [
			dtToolbar,
			{ height: 22},
			trackTreetable,
			{ height: 40 },
			{view: "toolbar", id: "viewToolbarID", height: 40, elements : [{ view:"label", id: "viewToolbarLabelID", css:".webix_ui_label_toolbar", label: data.viewLabelText}]},
			visitChart,
			{view: "toolbar", id: "timeToolbarID", height: 40, elements : [{ view:"label", id: "timeToolbarLabelID", css:".webix_ui_label_toolbar", label: data.timeLabelText}]},
			timeChart,
			{ height: 20 }
		]
	});

	if (data.visitChartData.length < 2) {
		$$("visitChartID").hide();
		$$("viewToolbarID").hide();
	}

	if (data.timeChartData.length < 2) {
		$$("timeChartID").hide();
		$$("timeToolbarID").hide();
	}

	webix.extend($$("trackTreetableID"), webix.ProgressBar);
	webix.extend($$("visitChartID"), webix.ProgressBar);
	webix.extend($$("timeChartID"), webix.ProgressBar);

	$$("trackTreetableID").showProgress({
		type:"bottom",
		delay:500,
		hide:true
	});

}
