function buildLeftMenu(data, containerID, callBack) {
	//  Левое меню
    webix.ui({
		view: "menu",
		css: "webix_ui_leftmenu",
		container: containerID,
		id: "leftMenuID",
		layout: "y",
		width: 150,
		autoheight:true,
		select: true,
		data: data.leftMenuData,
		on: {
			onMenuItemClick: function(id) {
				callBack(this.getMenuItem(id).id);
			}
		}
	});

}