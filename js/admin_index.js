function signin() {
    var login_val = $("#login").val();
    var password_val = $("#password").val();

    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                login: login_val,
                password: password_val,
            },
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            var id = 120;
            $.redirectGet("main.html", {
                code: hashCode(login_val + "/code/" + password_val)
            });
        });
}