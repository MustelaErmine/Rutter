let origin = window.location.origin;
let api_prefix = '/api'
let username = "{{username}}";

api_address = function (address) { return origin + api_prefix + address; }

function display_error(error) {
    var error_label = document.getElementById("error_alert");
    error_label.style = "";
    error_label.innerText = error;
}

async function try_register() {
    var username = document.forms.main.username.value;
    var password = document.forms.main.password.value;
    var password2 = document.forms.main.password2.value;
    if (username.length == 0 || password.length == 0) {
        display_error("Username or password is empty");
        return;
    }
    if (password != password2) {
        display_error("Passwords are not equal")
        return;
    }
    var response = await fetch(api_address("/user/register"),{method: 'POST', body: JSON.stringify({
        username: username,
        password: password,
        password2: password2
    })});
    var body = await response.text();
    if (response.status == 200) {
        window.location.replace("/enter");
    }
    else {
        console.log(body);
        display_error(body);
    }
}