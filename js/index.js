function signin() {
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    var is_editor = $('#editor').is(':checked');

    var home_page = is_editor ? "main_editor.html" : "main.html";

    $.ajax({
            url: "api/login",
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
                var id = response.id;
                $.redirectGet(home_page, {
                    user_id: id
                });
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
            $.redirectGet(home_page, {
                user_id: 120
            });
        });
}

function signin_doctor() {
    var name = $("#name").val();
    var email = $("#email").val();
    window.location.href = 'search.html?name=' + name + '&email=' + email;
}