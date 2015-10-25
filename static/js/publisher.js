function buildUI(data, containerID) {

	//  Левое меню
	var leftMenu = {
		view: "menu",
		id: "lm",
		layout: "y",
		width: 150,
		autoheight:true,
		select: true,
		data: data.leftMenuData,
		on: {
			onMenuItemClick: function(id) {
				document.location.href = data.leftMenuLinks[this.getMenuItem(id).id - 1]
			}
		}
	};

	//  Тулбар
	var dtToolbar = {
		view: "toolbar",
		width: 950,
		cols: [{
			view: "combo",
			id: "dtCOmbo",
			label: "Период",
			value: "Сегодня",
			yCount: "5",
			options: data.toolbarDates
		}, {}, {
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
		}, {
			view: "button",
			type: "iconButton",
			icon: "refresh",
			label: "Обновить",
			width: 120,
			align: "right",
			click: function() {alert()}
		}]

	}

	//  Таблица трекинга
	var trackTreetable = {
		view: "treetable",
		id: "trt",
		height: 350,
		scroll: "y",
		select: "row",
		hover: "dthover",
		columns: [{
			id: "id",
			header: "",
			css: {
				"text-align": "left"
			},
			width: 50
		}, {
			id: "name",
			width: 370,
			header: "Площадка",
			footer: {
				text: ""
			},
			template: "{common.treetable()} #value#"
		}, {
			id: "time",
			header: "Ср. время (мин.)",
			width: 165,
			css: {
				"text-align": "right"
			}
		}, {
			id: "active",
			header: "Активность (мин.)",
			width: 165,
			css: {
				"text-align": "right"
			}
		}, {
			id: "visits",
			header: "Посещения",
			width: 120,
			css: {
				"text-align": "right"
			}
		}, {
			id: "uniq",
			header: "Уникальные",
			width: 120,
			css: {
				"text-align": "right"
			}
		}],
		on:{
			"onItemClick":function(id, e, trg){
				//id.column - column id
				//id.row - row id
				alert("site: " + id.row);
			}
		},
		data: data.trackTreetableData
	};

	//График посещений
	var visitChart = {
		view: "chart",
		type: "line",
		height: 400,
		alpha: 0.7,
		xAxis: {
			template: "'#xAxis#"
		},
		yAxis: data.visitChartYAxis,
		legend: {
			values: data.visitChartLegendData,
			valign: "top",
			align: "center",
			layout: "x"
		},
		eventRadius: 5,
		series: [{
			type: "area",
			value: "#views#",
			color: "#a7ee70",
			tooltip: {
				template: "#views#"
			}
		}, {
			type: "line",
			value: "#views#",
			color: "#a7ee70",
			tooltip: {
				template: "#views#"
			}
		}, {
			type: "area",
			value: "#reqs#",
			color: "#36abee",
			tooltip: {
				template: "#reqs#"
			}
		}, {
			type: "line",
			value: "#reqs#",
			color: "#36abee",
			tooltip: {
				template: "#reqs#"
			}
		}],
		data: data.visitChartData
	}

	//График времени
	var timeChart = {
		view: "chart",
		type: "line",
		height: 400,
		alpha: 0.7,
		xAxis: {
			template: "'#xAxis#"
		},
		yAxis: data.timeChartYAxis,
		legend: {
			values: data.timeChartLegendData,
			valign: "top",
			align: "center",
			layout: "x"
		},
		eventRadius: 5,
		series: [{
			type: "area",
			value: "#views#",
			color: "#a7ee70",
			tooltip: {
				template: "#views#"
			}
		}, {
			type: "line",
			value: "#views#",
			color: "#a7ee70",
			tooltip: {
				template: "#views#"
			}
		}, {
			type: "area",
			value: "#reqs#",
			color: "#36abee",
			tooltip: {
				template: "#reqs#"
			}
		}, {
			type: "line",
			value: "#reqs#",
			color: "#36abee",
			tooltip: {
				template: "#reqs#"
			}
		}],
		data: data.timeChartData
	}

	/*
	var browserChart = {
    	view: "chart",
    	type: "pie",
    	value: "#percent#",
    	color: "#color#",
    	label: "#browser#",
    	pieInnerText: "#browser#",
    	shadow: 0,
    	data: data.browserChartData
    }
	*/

	/*
	var cityChart = {
    	view: "chart",
    	type: "pie",
    	value: "#percent#",
    	color: "#color#",
    	label: "#city#",
    	pieInnerText: "#city#",
    	shadow: 0,
    	data: data.cityChartData
    }
	*/

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
		cols: [{
			rows: [
				leftMenu, {}
			]
		},
		{ width: 20 },
		{
			rows: [
				dtToolbar,
				{ height: 20 },
				trackTreetable,
				{ height: 20 },
				{ view:"label", label: "График посещений"},
				visitChart,
				{ height: 20 },
				{ view:"label", label: "График времени"},
				timeChart
			]
		}]

	});

	$$("lm").select(1);
	$$("trt").select(1);
}
