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
            console.log(data);
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
    $.redirectGet("editor.html", {
        user_id: user_id,
        block_id: id
    });
}

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
            response = data;
            if (response.code == "OK") {
                var pieces = response.document;

                for (var i = 0; i < pieces.length; ++i) {
                    var text = pieces[i].txt;
                    var url_text = text_uri(text.join("\n\n"));

                    var translate = pieces[i].translated_txt;
                    var url_translate = text_uri(translate ? translate.join("\n\n") : "");

                    $("#blocks").append(`
                        <div class="col s12 m4 l4">
                            <div class="card">

                                <div class="card-content">
                                <span class="card-title">` + pieces[i].name + `</span>
                                
                                <div class="download-url-or">
                                <a href="` + url_text + `" download="original.txt" class="waves-effect waves-light btn green download-btn"><i class="material-icons left">file_download</i>Скачать отрывок</a>
                                </div>
                                <div class="download-url-or">
                                <a href="` + url_translate + `" download="translate.txt" class="waves-effect waves-green btn-flat download-btn"><i class="material-icons left">file_download</i>Скачать текущий перевод</a>
                                </div>
                                <p class="preview">` + text[0].slice(0, 150) + `</p>
                                </div>
                                <div class="card-action edit-btn">
                                <a onclick="edit_block('` + pieces[i]._id + `');" class="continue-tr">Продолжить перевод</a>
                                </div>
                            </div>
                        </div>
                    `);
                }
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

function close_modal() {
    $("#hint").hide();
    $("#get").hide();
    $("#paragraphs").empty();
    selected_paragraphs.clear();
}

var selected_paragraphs = new Set();
var selected_paragraphs_ids = [];
var selected_document = "";

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
}

function create_block() {
    var p = Array.from(selected_paragraphs).sort();
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
        console.log(user_id);
        $.ajax({
                url: "api/update_pieces",
                method: "POST",
                data: {
                    id: user_id,
                    document_id: selected_document,
                    pcid: pids.join(","),
                    to_language: "RUS"
                },
                dataType: "json"
            })
            .done(function(data) {
                console.log(data);
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

    for (var i = 0; i < pieces_dict[selected_document].length; ++i) {
        $("#paragraphs").append(`
        <div class="row paragraphs-flex" id="p` + pieces_dict[selected_document][i].number + `" ` + (pieces_dict[selected_document][i].freedom ? `onclick="select_paragraph(` + i + `, '` + pieces_dict[selected_document][i]._id + `');"` : ``) + `>
            <div class="col s1">
                <div style="background: ` + (pieces_dict[selected_document][i].freedom ? "#aaa" : "#fa0000") + ` !important;" class="indicator" id="bar` + i + `"></div>
            </div>
            <div class="col s11">
                <p class="slim">
                &nbsp;&nbsp;&nbsp;&nbsp;` + pieces_dict[selected_document][i].txt + `
                </p>
            </div>
        </div>
        `);
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
            console.log(data);
            response = data;
            if (response.code == "OK") {

                var list = response.document;
                for (var i = 0; i < list.length; ++i) {
                    var tags = list[i].doc.tags.split(",");
                    var tags_markup = "";
                    console.log(pieces_dict);
                    pieces_dict[list[i].doc._id] = list[i].pieces;

                    for (var j = 0; j < tags.length; ++j) {
                        tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                    }

                    var ready = list[i].pieces;
                    var total = list[i].doc.piece_number;
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

function list_languages() {
    for (var i = 0; i < languages.length; ++i) {
        $("#lang").append(`
            <option value="` + languages[i].code + `">` + languages[i].name + `</option>
        `);
    }

    $("#lang").change(function() {
        list_documents($(this).val());
    })
}

function init() {
    $('.modal').modal();
    $("#hint").hide();
    $("#get").hide();

    list_languages();
    $('select').formSelect();

    list_blocks();
}

$(document).ready(function() {
    check_user(init);
});