function buildLoginForm(containerID, registerCallback, loginCallback) {
    webix.ui({
        view: "form",
        id: "loginFormID",
        container: containerID,
        width: 480,
        height: 200,
        elements:[

            { view: "text", id: "userValueID", name:"username", label: "E-mail",
                invalidMessage:"Введите корректный E-mail!",
                bottomLabel: " "},

            { view: "text", id: "passValueID", name:"password", type: "password", label: "Password",
                bottomLabel: " "},
            { margin: 5, cols: [
                { view: "button", value: "Регистрация", click: registerCallback},
                { view: "button", value: "Вход" , type: "form", click: loginCallback}
            ]}
        ],
        rules:{
            "username": webix.rules.isEmail
        },
        on:{
            'onChange':function(newv, oldv){
                this.validate();
        }
    }
    });
}