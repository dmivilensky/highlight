function signin() {
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    var is_editor = $('#editor').is(':checked');

    var home_page = is_editor ? "main_editor.html" : "main.html";

    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                login: login_val,
                password: password_val,
                type: is_editor ? 1 : 0
            },
            dataType: "json"
        })
        .done(function(data) {
            var id = 120;
            $.redirectGet(home_page, {
                user_id: id
            });
        })
        .fail(function(jqXHR, status) {
            var id = 120;
            $.redirectGet(home_page, {
                user_id: id
            });
        });
}

function signin_doctor() {
    var name = $("#name").val();
    var email = $("#email").val();
    window.location.href = 'search.html?name=' + name + '&email=' + email;
}