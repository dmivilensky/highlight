function check_user(success) {
    code = findGetParameter("code");

    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                id: code
            },
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            if (code) {
                success();
            } else {
                $.redirectGet("index.html", {});
            }
        });
}

function approve_user(id) {
    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {},
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            load_users();
        });
}

function delete_user(id) {
    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {},
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            load_users();
        });
}

function load_users() {
    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {},
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            $("#users").empty();

            var users = [{
                    id: 0,
                    type: 1,
                    name: "Иванов Иван Иванович",
                    vk: "id25314918",
                    fb: "",
                    tg: ""
                },
                {
                    id: 1,
                    type: 0,
                    name: "Цезарь Гай Юлий" + getRandomInt(5),
                    vk: "id25314918",
                    fb: "100004811492599",
                    tg: ""
                },
                {
                    id: 2,
                    type: 0,
                    name: "Марк Антоний",
                    vk: "id25314918",
                    fb: "",
                    tg: ""
                },
                {
                    id: 3,
                    type: 1,
                    name: "Марк Брут",
                    vk: "id25314918",
                    fb: "",
                    tg: ""
                }
            ]

            for (var i = 0; i < users.length; ++i) {
                var social = "";
                if (users[i].vk != "")
                    social += `
                    <p>
                    VK: <a href="https://vk.com/` + users[i].vk + `">` + users[i].vk + `</a>
                    </p>
                    `;
                if (users[i].fb != "")
                    social += `
                    <p>
                    FB: <a href="https://www.facebook.com/profile.php?id=` + users[i].fb + `">` + users[i].fb + `</a>
                    </p>
                    `;
                if (users[i].tg != "")
                    social += `
                    <p>
                    TG: <a>` + users[i].tg + `</a>
                    </p>
                    `;

                $("#users").append(`
                    <li class="collection-item avatar" style="padding-left: 20px;">
                    <p style="font-size: 12px; font-family: Consolas, monaco, monospace;">` + (users[i].type == 0 ? 'Переводчик' : 'Редактор') + `</p>
                    <span class="title">` + users[i].name + `</span>
                    ` + social + `
                    <div class="secondary-content">
                    <a onclick="approve_user(` + users[i].id + `);" style="margin-right: 20px;"><i class="material-icons green-text">done</i></a>
                    <a onclick="delete_user(` + users[i].id + `);"><i class="material-icons red-text">clear</i></a>
                    </div>
                    
                    </li>
                `);
            }
        });
}

function init() {
    $('.chips-autocomplete').chips({
        data: [{
            tag: 'Важный',
        }],
        autocompleteOptions: {
            data: {
                'Важный': null,
            },
            limit: Infinity,
            minLength: 1
        }
    });

    load_users();
}

$(document).ready(function() {
    check_user(init);
});