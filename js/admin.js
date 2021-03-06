var key_;

function check_user(success) {
    login_ = findGetParameter("login");
    password_ = findGetParameter("password");
    key_ = findGetParameter("code");

    $.ajax({
            url: "/api/let_my_people_pass",
            method: "POST",
            data: {
                login: login_,
                password: password_
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK" && response.key == key_) {
                success();
            } else {
                $.redirectGet("index.html", {});
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
            $.redirectGet("index.html", {});
        });
}

function approve_user(login) {
    $.ajax({
            url: "/api/verify",
            method: "POST",
            data: {
                key: key_,
                decision: 1,
                login: login
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                load_users();
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function delete_user(login) {
    $.ajax({
            url: "/api/verify",
            method: "POST",
            data: {
                key: key_,
                decision: 0,
                login: login
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                load_users();
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function load_users() {
    $.ajax({
            url: "/api/get_users",
            method: "POST",
            data: { key: key_ },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                $("#users").empty();
                var users = response.document;

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
                    if (users[i].email != "")
                        social += `
                        <p>
                        e-mail: <a>` + users[i].email + `</a>
                        </p>
                        `;

                    var status_string = "";
                    if (users[i].status == "translator") {
                        status_string = "Переводчик";
                    } else if (users[i].status == "chief") {
                        status_string = "Редактор";
                    } else if (users[i].status == "both") {
                        status_string = "Переводчик, Редактор";
                    } else {
                        status_string = "Верстальщик";
                    }

                    $("#users").append(`
                        <li class="collection-item avatar user-card">
                        <p class="user-status">` + status_string + `</p>
                        <span class="title">` + users[i].name + `</span>
                        ` + social + `
                        <div class="secondary-content">
                        <a onclick="approve_user('` + users[i].login + `');" class="approve-btn"><i class="material-icons green-text">done</i></a>
                        <a onclick="delete_user('` + users[i].login + `');"><i class="material-icons red-text">clear</i></a>
                        </div>
                        
                        </li>
                    `);
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

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

function load_languages() {
    $("#lang").empty();
    for (var i = 0; i < languages.length; ++i) {
        $("#lang").append(`
        <div class="col s6 m4 l4">
            <p><label>
                <input type="radio" name="group1" id="lang_` + i + `" ` + (i == 0 ? `checked` : ``) + ` />
                <span>` + languages[i].name + `</span>
            </label></p>
        </div>
        `);
    }
}

function reset_all() {
    $('#abstract').val(null);
    $('#author').val(null);
    $('#jour').val(null);
    $('#jl').val(null);
    $("#file").trigger("reset");
    $("#fname").val(null);
    is_edited = false;
    abstract = "";
    author = "";
    journal = "";
    jl = "";
    tags_field.chips({
        data: [{
            tag: 'Теги и ключевые слова',
        }],
        autocompleteOptions: {
            data: {
                'Теги и ключевые слова': null,
            },
            limit: Infinity,
            minLength: 1
        }
    });
}

async function add_document() {
    var lang = "";
    var lang_set = false;
    for (var i = 0; i < languages.length; ++i) {
        if ($("#lang_" + i).is(':checked')) {
            lang_set = true;
            lang = languages[i].code;
            break;
        }
    }

    if (!lang_set) {
        lang = $("#lang_other_val").val();
    }

    var chips = M.Chips.getInstance($('#tags')).chipsData;
    var tags_ = "";
    for (var i = 0; i < chips.length; ++i) {
        tags_ += chips[i].tag + ",";
    }
    tags_ = tags_.slice(0, -1);
    if (is_edited == false) {
        tags_ = "";
    }

    var real_name = $("#filename");
    var extention = real_name.val().slice(-3, -1) + real_name.val().slice(-1);
    if (extention != "pdf") {
        alert("Необходимо загрузить .pdf файл!");
    } else {
        var fname = 'new_file' + getRandomInt(10000) + '.pdf';
        $("#filename").val(fname);

        var finame = $("#fname").val();
        if (finame.trim() == "") {
            finame = real_name.val().slice(0, -5);
        }

        $('#file').on('submit', function(event) {
            event.preventDefault();

            // console.log("forming form");
            var post_data = new FormData($("#file")[0]);
            post_data.append("name", finame);
            post_data.append("language", lang);
            post_data.append("tags", tags_);
            // console.log("adding abstract \n" + abstract + "\n" + author + "\n" + journal + "\n" + jl.toString() + "\n");
            post_data.append("abstract", abstract);
            post_data.append("author", author);
            post_data.append("journal", journal);
            post_data.append("jl", jl.toString());
            post_data.append("key", key_);
            // console.log("finish");

            $.ajax({
                xhr: function() {
                    var xhr = new window.XMLHttpRequest();

                    // console.log("uploading");

                    xhr.upload.addEventListener("progress", function(evt) {
                        var percent = Math.round(evt.loaded / evt.total * 100);
                        $('#submitting_button').attr('disabled', true);
                        $('#submitting_button').get(0).innerText = "Загружено: " + percent + '%';
                        // console.log("preloading")
                    }, false);

                    xhr.upload.addEventListener("load", function(evt) {
                        $('#submitting_button').css('background-color', 'green').delay(2000);
                        $('#submitting_button').get(0).innerText = "Готово, ждём ответа сервера...";
                        // console.log("loading")
                    }, false);

                    return xhr;
                },
                url: "/api/update_docs",
                type: "POST",
                data: post_data,
                processData: false,
                contentType: false,
                success: function(result) {
                    $('#submitting_button').attr('disabled', false);
                    alert("Файл загружен!");
                    $('#submitting_button').get(0).innerText = "ЗАГРУЗИТЬ ФАЙЛ";
                    reset_all();
                    location.reload();
                }
            });
            event.stopImmediatePropagation();
        });

        $("#file").submit();
    }
}

function load_stat() {
    $.ajax({
            url: "/api/get_trans_and_docs",
            method: "POST",
            data: {
                key: key_
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                var stat = response.document;
                $("#stat_untranslated").html(stat.documents);
                $("#stat_translated").html(stat.translated_documents);
                $("#stat_users").html(stat.translators);
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function load_work() {
    $.ajax({
            url: "/api/get_pieces_stat",
            method: "POST",
            data: { key: key_ },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            $("#work").empty();

            // TODO document_S_
            for (var i = 0; i < response.document.length; ++i) {
                var name = response.document[i].translator;
                var document = "«" + response.document[i].name + "»";
                var date = response.document[i].date.split(" ")[0];
                var pb = response.document[i].pb;
                var pe = response.document[i].pe;

                $("#work").append(`
                <tr>
                    <td>` + name + `</td>
                    <td>` + document + (pb == pe ? `<br>Страницы: ` + pb + `-` + pe : `<br>Страница: ` + pb) + `</td>
                    <td>` + date + `</td>
                </tr>
                `);
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function load_translators() {
    $.ajax({
            url: "/api/get_translator_stats",
            method: "POST",
            data: {
                key: key_
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                $("#translators").empty();

                var data_translator = response.document;
                for (var i = 0; i < data_translator.length; ++i) {
                    var name = data_translator[i].name;
                    var paragraphs = 0;
                    for (var j = 0; j < data_translator[i].pieces.length; ++j) {
                        paragraphs += data_translator[i].pieces[j].indexes.length;
                    }

                    var vk = data_translator[i].vk;
                    var fb = data_translator[i].fb;
                    var tg = data_translator[i].tg;

                    var social_markup = "";
                    if (vk && vk != "") {
                        social_markup += "VK: " + vk + "<br>";
                    }
                    if (fb && fb != "") {
                        social_markup += "FB: " + fb + "<br>";
                    }
                    if (tg && tg != "") {
                        social_markup += "TG: " + tg + "<br>";
                    }
                    social_markup = social_markup.slice(0, -4);

                    $("#translators").append(`
                            <tr>
                                <td>` + name + `<br>` + social_markup + `</td>
                                <td>` + paragraphs + `</td>
                            </tr>`);
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function load_coworkers(id) {
    $.ajax({
            url: "/api/get_coworkers",
            method: "POST",
            data: {
                find_id: id
            },
            dataType: "json"
        })
        .done(function(data) {
            $("#cow" + id).empty();
            $("#cow" + id).append('Переводчики: <br>');
            response = data;
            if (response.code == "OK") {
                for (var i = 0; i < response.document.length; ++i) {
                    var social = "";
                    if (response.document[i].vk != "") {
                        social += 'vk: ' + response.document[i].vk + ', '
                    }
                    if (response.document[i].fb != "") {
                        social += 'fb: ' + response.document[i].fb + ', '
                    }
                    if (response.document[i].tg != "") {
                        social += 'tg: ' + response.document[i].tg + ', '
                    }
                    social = social.slice(0, -2);
                    $("#cow" + id).append(response.document[i].name + '<br>' + response.document[i].email + ', ' + social + '<br><br>');
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function load_documents() {
    $.ajax({
            url: "/api/get_file_stat",
            method: "POST",
            data: {
                key: key_
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                $("#documents").empty();

                var data_doc = response.document;
                for (var i = 0; i < data_doc.length; ++i) {
                    var document = "«" + data_doc[i].name + "»";
                    var status = data_doc[i].status;
                    var paragraphs_all = data_doc[i].pieces_info.all_pieces;
                    var paragraphs_ready = data_doc[i].pieces_info.done_pieces;
                    var stars = data_doc[i].importance;

                    var status_text = "";
                    switch (status) {
                        case 'TRANSLATED':
                            status_text = "Переведён и проверен";
                            break;
                        case 'NEED_CHECK':
                            status_text = "Переведён";
                            break;
                        case 'WAITING_FOR_TRANSLATION':
                            status_text = "В работе<br>(переведено " + paragraphs_ready + "/" + paragraphs_all + " страниц)";
                    }

                    load_coworkers(data_doc[i]._id);
                    $("#documents").append(`
                            <tr>
                                <td>` + document + `</td>
                                <td>` + status_text + `<br><span id="cow` + data_doc[i]._id + `"></span></td>
                                <td>` + stars + `</td>
                                <td class="corner"><a onclick="delete_file('` + data_doc[i]._id + `');" class="secondary-content"><i class="material-icons red-text">clear</i></a></td>
                            </tr>
                    `);
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function delete_file(id) {
    $("#documents").empty();
    $.ajax({
            url: "/api/delete",
            method: "POST",
            data: {
                key: key_,
                document_id: id
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            load_documents();
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

function save_db() {
    $.ajax({
            url: "/api/get_translator_stats",
            method: "POST",
            data: {
                key: key_
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                var db_data = [];

                var data_translator = response.document;
                for (var i = 0; i < data_translator.length; ++i) {
                    var name = data_translator[i].name;
                    var email = data_translator[i].email;
                    var status = data_translator[i].status;
                    var langs = data_translator[i].langs;
                    var paragraphs = data_translator[i].translated;

                    var vk = data_translator[i].vk;
                    var fb = data_translator[i].fb;
                    var tg = data_translator[i].tg;

                    var social_markup = "";
                    if (vk && vk != "") {
                        social_markup += "VK: " + vk + ";";
                    }
                    if (fb && fb != "") {
                        social_markup += "FB: " + fb + ";";
                    }
                    if (tg && tg != "") {
                        social_markup += "TG: " + tg + ";";
                    }
                    social_markup = social_markup.slice(0, -4);

                    db_data.push(name + ";" + status + ";" + langs + ";" + email + ";" + social_markup + ";" + paragraphs);
                }

                db_data.sort(function(a, b) { return a.localeCompare(b); });
                download_text(db_data.join("\n"), "users_db.txt");
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}
var abstract = "";
var author = "";
var journal = "";
var jl = "";
function add_abstract() {
    abstract = $('#abstract').val();
    author = $('#author').val();
    journal = $('#jour').val();
    jl = $('#jl').val();
    alert("Данные добавлены");
}

var tags_field;
var is_edited = false;
function init() {
    tags_field = $('#tags');
    tags_field.chips({
        data: [{
            tag: 'Теги и ключевые слова',
        }],
        autocompleteOptions: {
            data: {
                'Теги и ключевые слова': null,
            },
            limit: Infinity,
            minLength: 1
        }
    });
    $('.modal').modal();
    tags_field.click(function(){
        if (!is_edited) {
            is_edited = true;
            tags_field.chips({
                autocompleteOptions: {
                    limit: Infinity,
                    minLength: 1
                }
            });
        }
    });

    load_languages();
    load_users();
    load_stat();
    load_work();
    load_translators();
    load_documents();
}

$(document).ready(function() {
    //csrf_setup();
    check_user(init);
    // init()
});