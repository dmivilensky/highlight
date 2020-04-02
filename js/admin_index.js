function signin() {
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    $.ajax({
            url: "/api/let_my_people_pass",
            method: "POST",
            data: {
                login: login_val,
                password: password_val
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            response = data;
            if (response.code == "OK") {
                $.redirectGet("main.html", {
                    code: response.key,
                    login: login_val,
                    password: password_val
                });
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}