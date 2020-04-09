var user_id = "";

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

function check_user(success) {
    user_id = findGetParameter("user_id");

    $.ajax({
            url: "api/check_user",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK" && response.result) {
                success();
            } else {
                $.redirectGet("index.html", {});
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
            $.redirectGet("index.html", {});
        });
}

function edit_block(id) {
    list_blocks();
}

var inserted = [];

function list_blocks() {
    $.ajax({
            url: "api/find_pieces",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            $("#blocks").empty();
            $("#blocks_ready").empty();
            inserted = [];

            response = data;
            if (response.code == "OK") {
                var pieces = response.document;

                for (var i = 0; i < pieces.length; ++i) {
                    if (inserted.includes(pieces[i]._id)) {
                        continue;
                    }

                    inserted.push(pieces[i]._id);
                    var text = pieces[i].txt_path;
                    var translate = pieces[i].translated_txt_path;

                    if (pieces[i].translation_status == "DONE") {
                        $("#blocks_ready").append(`
                            <div class="col s12 m4 l4">
                                <div class="card">

                                    <div class="card-content">
                                    <span class="mono">Переведено</span>
                                    <span class="card-title">` + pieces[i].name + `</span>
                                    <p>Этот файл также переводят:</p>
                                    <p id="others` + pieces[i]._id + `"></p>
                                    
                                    <div class="download-url-or">
                                    <a href="./files/` + text + `" download="` + text + `" class="waves-effect waves-green btn-flat download-btn ready-btn"><i class="material-icons left">file_download</i>Скачать отрывок</a>
                                    </div>
                                    <div class="download-url-or">
                                    <a href="./files/` + translate + `" download="` + translate + `" class="waves-effect waves-green btn-flat download-btn ready-btn"><i class="material-icons left">file_download</i>Скачать перевод</a>
                                    </div>
                                </div>
                            </div>
                        `);
                    } else {
                        $("#blocks").append(`
                            <div class="col s12 m4 l4">
                                <div class="card">

                                    <div class="card-content">
                                    <span class="card-title">` + pieces[i].name + `</span>
                                    <p>Этот файл также переводят:</p>
                                    <p id="others` + pieces[i]._id + `"></p>
                                    
                                    <div class="download-url-or">
                                    <a href="./files/` + text + `" download="` + text + `" class="waves-effect waves-light btn green download-btn"><i class="material-icons left">file_download</i>Скачать отрывок</a>
                                    </div>
                                    <div class="download-url-or">
                                    <a href="./files/` + translate + `" download="` + translate + `" class="waves-effect waves-green btn-flat download-btn ready-btn"><i class="material-icons left">file_download</i>Скачать текущий перевод</a>
                                    </div>
                                    <div class="download-url-or">
                                    <a onclick="ready('` + pieces[i]._id + `')"class="waves-effect waves-light btn yellow lighten-4 download-btn black-text"><i class="material-icons left">done_all</i>Завершить перевод</a>
                                    </div>
                                    </div>
                                    <div class="card-action edit-btn">
                                    <a onclick="update_tr('` + pieces[i]._id + `')" class="continue-tr">Обновить перевод</a><br>
                                    </div>
                                </div>
                            </div>
                        `);
                    }
                    load_others(pieces[i]._id);

                }
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

function load_others(id) {
    for (var i = 0; i < 5; ++i) {
        var social = "";
        if (true) {
            social += 'vk: ' + 'vk' + '<br>'
        }
        $('#others' + id).append('Иванов Иван Иванович' + 'ivan@ivan.ru' + '<br>' + social);
    }
}

var current_block = '';

function update_tr(block_id) {
    current_block = block_id;
    $('#modal2').modal('open');
}

function upload() {
    var fname = 'new_file' + getRandomInt(10000) + '.docx';
    $("#corrections_path").val(fname);

    $('#file').on('submit', function(event) {
        // event.preventDefault();

        var post_data = new FormData($("#file")[0]);
        post_data.append("id", user_id);
        post_data.append("piece_id", current_block);

        $.ajax({
            xhr: function() {
                var xhr = new window.XMLHttpRequest();

                xhr.upload.addEventListener("progress", function(evt) {
                    var percent = Math.round(evt.loaded / evt.total * 100);
                    console.log(percent);
                    $('#submitting_button').attr('disabled', true);
                    $('#submitting_button').get(0).innerText = "Загружено: " + percent + '%'
                }, false);

                xhr.upload.addEventListener("load", function(evt) {
                    $('#submitting_button').css('background-color', 'green').delay(2000);
                    $('#submitting_button').get(0).innerText = "Готово, ждём ответа сервера..."

                }, false);

                return xhr;
            },

            url: "/api/update_translating_pieces",
            type: "POST",
            data: post_data,
            processData: false,
            contentType: false,
            success: function(result) {
                $('#submitting_button').attr('disabled', false);
                alert("Файл загружен!");
                $('#submitting_button').get(0).innerText = "ЗАГРУЗИТЬ ФАЙЛ";
                list_blocks();
            }
        });
    });
    $("#file").submit();
}

function ready(block_id) {
    if (confirm("Вы действительно хотите подтвердить текущий перевод?")) {
        $.ajax({
                url: "api/update_translating_pieces",
                method: "POST",
                data: {
                    id: user_id,
                    piece_id: block_id,
                    status: "DONE"
                },
                dataType: "json"
            })
            .done(function(data) {
                response = data;
                if (response.code == "OK") {
                    list_blocks();
                }
            })
            .fail(function(jqXHR, status, error) {
                console.log(error);
            });
    }
}

function close_modal() {
    $('#modal1').modal('close');
    $("#hint").hide();
    $("#get").hide();
    $("#paragraphs").empty();
    $("#docs").empty();
    $("#lang").formSelect();
    $("#lang").change(function() {
        list_documents($(this).val());
    })
    list_documents('ENG');
    selected_paragraphs.clear();
}

var selected_paragraphs = new Set();
var selected_paragraphs_ids = [];
var selected_document = "";
var max_checked = -1;

var pieces_dict = {};

function select_paragraph(i, id) {
    if ($("#bar" + i).css("background-color") == "rgb(76, 175, 80)") {
        selected_paragraphs.delete(i);
        $("#bar" + i).css("background-color", "#aaaaaa");
    } else {
        selected_paragraphs.add(i);
        selected_paragraphs_ids[i] = id;
        $("#bar" + i).css("background-color", "#4caf50");
    }

    if (i > max_checked) {
        var all_enable = true;
        for (var j = max_checked + 1; j < i; ++j) {
            if ($("#status" + j).html() == "not") {
                all_enable = false;
                break;
            }
        }
        if (all_enable) {
            for (var j = max_checked + 1; j < i; ++j) {
                selected_paragraphs.add(j);
                selected_paragraphs_ids[j] = $("#status" + j).html();
                $("#bar" + j).css("background-color", "#4caf50");
            }
        }
        max_checked = i;
    }
}

function create_block() {
    if (selected_paragraphs.size == 0) {
        return;
    }

    var p = Array.from(selected_paragraphs).sort(function(a, b) { return a - b });
    selected_paragraphs.clear();
    var all_correct = true;
    for (var i = 1; i < p.length; ++i) {
        if (p[i] - p[i - 1] != 1) {
            all_correct = false;
            break;
        }
    }

    var pids = [];
    for (var i = 0; i < p.length; ++i) {
        pids.push(selected_paragraphs_ids[p[i]]);
    }

    if (!all_correct) {
        alert("Выбирать можно только последовательно идущие абзацы!");
    } else {
        console.log(pids);
        $.ajax({
                url: "api/update_pieces",
                method: "POST",
                data: {
                    id: user_id,
                    document_id: selected_document,
                    pcid: pids.join("#del#"),
                    to_language: "RUS"
                },
                dataType: "json"
            })
            .done(function(data) {
                // console.log(data);
                response = data;
                if (response.code == "OK") {
                    close_modal();
                    edit_block(response.id);
                }
            })
            .fail(function(jqXHR, status, error) {
                console.log(error);
            });
    }
}

function select_document(id) {
    $("#hint").show();
    $("#get").show();
    $("#paragraphs").empty();
    selected_paragraphs.clear();

    selected_document = id;
    $("#get").click(create_block);

    console.log(pieces_dict[selected_document]);
    for (var i = 0; i < pieces_dict[selected_document].length; ++i) {
        $("#paragraphs").append(`
        <div class="row paragraphs-flex" id="p` + pieces_dict[selected_document][i].number + `" ` + (pieces_dict[selected_document][i].freedom ? `onclick="select_paragraph(` + i + `, '` + pieces_dict[selected_document][i]._id + `');"` : ``) + `>
            <div class="col s1">
                <div style="background: ` + (pieces_dict[selected_document][i].freedom ? "#aaa" : "#fa0000") + ` !important;" class="indicator" id="bar` + i + `"></div>
                <div id="status` + i + `" style="visibility: hidden;">` + (pieces_dict[selected_document][i].freedom ? pieces_dict[selected_document][i]._id : "not") + `</div>
            </div>
            <div class="col s11">
                <p class="slim">
                <canvas id="canvas` + pieces_dict[selected_document][i]._id + `" style="border:1px solid black"></canvas>
                </p>
            </div>
        </div>
        `);
        load_pdf_pages('files/' + pieces_dict[selected_document][i].txt_path, 'canvas' + pieces_dict[selected_document][i]._id, 0.7);
    }
}

function list_documents(lang) {
    $("#hint").hide();
    $("#get").hide();
    $("#paragraphs").empty();
    $("#docs").empty();

    $.ajax({
            url: "api/find_doc_by_lang",
            method: "POST",
            data: {
                language: lang
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {

                var list = response.document;
                for (var i = 0; i < list.length; ++i) {
                    var tags = list[i].doc.tags.split(",");
                    var tags_markup = "";
                    pieces_dict[list[i].doc._id] = list[i].pieces;

                    for (var j = 0; j < tags.length; ++j) {
                        tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                    }

                    var total = list[i].doc.piece_number;
                    var ready = 0;
                    for (var j = 0; j < total; ++j) {
                        if (!list[i].pieces[j].freedom) {
                            ready += 1;
                        }
                    }
                    var progress = ((ready / total) * 100).toFixed(1) + "%";

                    $("#docs").append(`
                        <li class="collection-item avatar" onclick="select_document('` + list[i].doc._id + `');">
                        <i class="material-icons circle">schedule</i>
                        <p>
                        ` + list[i].name + `
                        </p>
                        <div class="progress-bg"></div>
                        <div class="progress-ind" style="width: ` + progress + `;"></div>
                        <div class="tags-par">
                        ` + tags_markup + `
                        </div>
                        </li>
                    `);
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

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

function add_social_val(i, vv) {
    $('#soc').append(`
        <div id="field` + social_idx + `" class="spec">
        <div class="input-field col s12 m12 l4">
            <select class="soc" id="soc_value` + social_idx + `">
            <option value="1" ` + (i == 1 ? `selected` : ``) + `>ВК</option>
            <option value="2" ` + (i == 2 ? `selected` : ``) + `>Facebook</option>
            <option value="3" ` + (i == 3 ? `selected` : ``) + `>Telegram</option>
            </select>
            <label>Соц. сеть</label>
        </div>

        <div class="input-field col s12 m12 l8">
            <input id="soc` + social_idx + `" value="` + vv + `" type="text" class="validate">
            <label for="soc` + social_idx + `">id</label>
        </div>
        </div>
    `);
    $('select').formSelect();
    ++social_idx;
}

var oname = "";
var olang = "";

function load_acc() {
    $('#soc').empty();
    $.ajax({
            url: "api/get_account",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            console.log(data);
            if (response.code == "OK") {
                oname = response.document.name;
                $("#name").val(oname);
                olang = response.document.langs;
                var lls = olang.split(',');
                list_ll(lls);
                $("#email").val(response.document.email);
                $("#login").val(response.document.login);
                if (response.document.vk.trim() != "") {
                    add_social_val(1, response.document.vk);
                }
                if (response.document.fb.trim() != "") {
                    add_social_val(2, response.document.fb);
                }
                if (response.document.tg.trim() != "") {
                    add_social_val(3, response.document.tg);
                }
                M.updateTextFields();
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

function update_profile() {
    var verifiable = false;

    var name_val = $("#name").val();
    var email_val = $("#email").val();
    var login_val = $("#login").val();
    var password_val = $("#password").val();
    var password_now_val = $("#password_now").val();

    var post_dt = {
        id: user_id
    };
    if (password_now_val.trim() != "") {
        post_dt["password"] = password_now_val
    } else {
        alert('Необходимо ввести текущий пароль.');
        return;
    }

    if (name_val.trim() != "" && name_val.trim() != oname) {
        post_dt["name"] = name_val;
        verifiable = true;
    }
    if (email_val.trim() != "") {
        post_dt["email"] = email_val;
    }
    if (login_val.trim() != "") {
        post_dt["login"] = login_val;
    }
    if (password_val.trim() != "") {
        post_dt["npassword"] = password_val;
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

    if (vk_.trim() != "") {
        post_dt["vk"] = vk_
    }
    if (fb_.trim() != "") {
        post_dt["fb"] = fb_
    }
    if (tg_.trim() != "") {
        post_dt["tg"] = tg_
    }

    var lang = "";
    for (var i = 0; i < languages.length; ++i) {
        if ($('#langf' + i).is(':checked')) {
            lang += languages[i].code + ",";
        }
    }
    lang = lang.slice(0, -1);

    if (lang.trim() != "" && lang.trim() != olang) {
        post_dt["languages"] = lang;
        verifiable = true;
    }

    console.log(post_dt);
    $('#modal3').modal('close');
    $.ajax({
            url: "api/update_account",
            method: "POST",
            data: post_dt,
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                if (verifiable) {
                    if (confirm('Заявка отправлена, вы сможете войти после подтверждения изменившихся данных.')) {
                        $.redirectGet('index.html');
                    } else {
                        $.redirectGet('index.html');
                    }
                } else {
                    alert('Данные изменены!');
                    load_acc();
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

function list_languages() {
    $("#lang").append(`
        <option value="` + languages[0].code + `" selected>` + languages[0].name + `</option>
    `);
    for (var i = 1; i < languages.length; ++i) {
        $("#lang").append(`
            <option value="` + languages[i].code + `">` + languages[i].name + `</option>
        `);
    }
    drg = "Другой";
    oth = "OTH"
    $("#lang").append(`
            <option value="` + oth + `">` + drg + `</option>
        `);

    $("#lang").change(function() {
        list_documents($(this).val());
    })
}

function list_ll(list) {
    $("#langf").empty();
    for (var i = 0; i < languages.length; ++i) {
        $("#langf").append(`
        <div class="col s12 m4 l4">
            <p><label>
                <input type="checkbox" id="langf` + i + `"  ` + (list.includes(languages[i].code) ? ` checked="checked"` : ``) + ` />
                <span>` + languages[i].name + `</span>
            </label></p>
        </div>
        `);
    }
}

function init() {
    $('.modal').modal();
    $("#hint").hide();
    $("#get").hide();

    list_languages();
    $('select').formSelect();
    list_documents('ENG');

    list_blocks();

    list_ll([]);
    load_acc();
}

$(document).ready(function() {
    check_user(init);
});