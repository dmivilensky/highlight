var languages = [{
    code: "ENG",
    name: "Английский"
}, {
    code: "GER",
    name: "Немецкий"
}, {
    code: "FRE",
    name: "Французский"
}, {
    code: "ESP",
    name: "Испанский"
}, {
    code: "ITA",
    name: "Итальянский"
}, {
    code: "JAP",
    name: "Японский"
}, {
    code: "CHI",
    name: "Китайский"
}];

$(document).ready(function() {
    $('select').formSelect();

    for (var i = 0; i < languages.length; ++i) {
        $("#lang").append(`
        <div class="col s12 m4 l4">
            <p><label>
                <input type="checkbox" id="lang` + i + `" />
                <span>` + languages[i].name + `</span>
            </label></p>
        </div>
        `);
    }
});

var social_idx = 1;

function remove_social() {
    if (social_idx > 1) {
        --social_idx;
        $('#field' + social_idx).remove();
    }
}

function add_social() {
    $('#soc').append(`
        <div id="field` + social_idx + `">
        <div class="input-field col s12 m12 l4">
            <select class="soc" id="soc_value` + social_idx + `">
            <option value="1" selected>ВК</option>
            <option value="2">Facebook</option>
            <option value="3">Telegram</option>
            </select>
            <label>Соц. сеть</label>
        </div>

        <div class="input-field col s12 m12 l8">
            <input id="soc` + social_idx + `" type="text" class="validate">
            <label for="soc` + social_idx + `">id</label>
        </div>
        </div>
    `);
    $('select').formSelect();
    ++social_idx;
}

function signup() {
    var name_val = $("#name").val();
    var email_val = $("#email").val();
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    var is_editor = $('#editor').is(':checked');
    var is_translator = $('#translator').is(':checked');

    var status_ = "";
    if (is_editor && is_translator) {
        status_ = "both";
    } else if (is_editor) {
        status_ = "chief";
    } else {
        status_ = "translator";
    }

    var vk_ = "";
    var fb_ = "";
    var tg_ = "";

    for (var i = 0; i < social_idx; ++i) {
        if ($("#soc_value" + i).val() == "1") {
            if (vk_ == "")
                vk_ = $("#soc" + i).val();
        }
        if ($("#soc_value" + i).val() == "2") {
            if (fb_ == "")
                fb_ = $("#soc" + i).val();
        }
        if ($("#soc_value" + i).val() == "3") {
            if (tg_ == "")
                tg_ = $("#soc" + i).val();
        }
    }

    var lang = "";
    for (var i = 0; i < languages.length; ++i) {
        if ($('#lang' + i).is(':checked')) {
            lang += languages[i].code + ",";
        }
    }
    lang = lang.slice(0, -1);

    var home_page = is_editor ? "main_editor.html" : "main.html";
    $.ajax({
            url: "api/registration",
            method: "POST",
            data: {
                name: name_val,
                surname: "",
                mi: "",
                email: email_val,
                languages: lang,
                login: login_val,
                password: password_val,
                status: status_,
                vk: vk_,
                fb: fb_,
                tg: tg_
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
            } else if (response.code == "1000") {
                alert("Пользователь с таким логинов уже существует!");
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}