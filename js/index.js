function try_signin_both() {
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    var is_editor = $('#editor').is(':checked');

    var home_page = is_editor ? "main_editor.html" : "main.html";

    //csrf_setup();

    $.ajax({
            url: "api/login",
            method: "POST",
            data: {
                login: login_val,
                password: password_val,
                type: "both"
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                var id = response.id;
                $.redirectGet(home_page, {
                    user_id: id
                });
            } else if (response.code == "2001") {
                alert("Неверный пароль!");
            } else if (response.code == "2000") {
                alert("Неверный логин!");
            } else if (response.code == "2002") {
                alert("Аккаунт пока не подтверждён.");
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function signin() {
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    var is_editor = $('#editor').is(':checked');
    var is_markup = $('#markup').is(':checked');

    //csrf_setup();

    if (login_val.trim() == "") {
        alert("Необходимо ввести логин.");
        return;
    }
    if (password_val.trim() == "") {
        alert("Необходимо ввести пароль.");
        return;
    }

    var home_page = "";
    if (is_editor) {
        home_page = "main_editor.html";
    } else if (is_markup) {
        home_page = "main_markup.html"
    } else {
        home_page = "main.html"
    }
    var status = "";
    if (is_editor) {
        status = "chief";
    } else if (is_markup) {
        status = "verif"
    } else {
        status = "translator"
    }

    $.ajax({
            url: "api/login",
            method: "POST",
            data: {
                login: login_val,
                password: password_val,
                type: status
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                var id = response.id;
                $.redirectGet(home_page, {
                    user_id: id
                });
            } else if (response.code == "2002") {
                alert("Аккаунт пока не подтверждён.");
            } else {
                try_signin_both();
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function signin_doctor() {
    var name = $("#name").val();
    var email = $("#email").val();
    window.location.href = 'search.html?name=' + name + '&email=' + email;
}