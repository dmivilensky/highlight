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
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            if (user_id == 120) {
                success();
            } else {
                $.redirectGet("index.html", {});
            }
        });
}

function edit_block(id) {
    $.redirectGet("editor.html", {
        user_id: user_id,
        block_id: id
    });
}

function list_blocks() {
    for (var i = 0; i < 5; ++i) {
        var id = i;
        var title = "«" + "Disinfection instructions" + "»";
        var text = [
            `I am a very simple card. I am good at containing small bits of information.`,
            `I am convenient because I require little markup to use effectively.I am a very simple card. I am good at containing small bits of information.`,
            `I am convenient because`
        ];
        var url_text = text_uri(text.join("\n\n"));

        var translate = [
            `FFF I am a very simple card. I am good at containing small bits of information.`,
            `I am convenient because I require little markup to use effectively.I am a very simple card. I am good at containing small bits of information.`,
            `I am convenient because`
        ];
        var url_translate = text_uri(translate.join("\n\n"));

        var tags = ["Английский", "Дезинфекция", "Массачусетс", "Городские мероприятия"];

        var tags_markup = "";
        for (var j = 0; j < tags.length; ++j) {
            tags_markup += `<div class="chip">` + tags[j] + `</div>`;
        }

        $("#blocks").append(`
                <div class="col s12 m4 l4">
                    <div class="card">

                        <div class="card-content">
                        <span class="card-title">` + title + `</span>
                        
                        <div class="tags-markup">
                        ` + tags_markup + `
                        </div>
                        <div class="download-url-or">
                        <a href="` + url_text + `" download="original.txt" class="waves-effect waves-light btn green download-btn"><i class="material-icons left">file_download</i>Скачать отрывок</a>
                        </div>
                        <div class="download-url-or">
                        <a href="` + url_translate + `" download="translate.txt" class="waves-effect waves-green btn-flat download-btn"><i class="material-icons left">file_download</i>Скачать текущий перевод</a>
                        </div>
                        <p class="preview">` + text[0].slice(0, 150) + `</p>
                        </div>
                        <div class="card-action edit-btn">
                        <a onclick="edit_block(` + id + `);" class="continue-tr">Продолжить перевод</a>
                        </div>
                    </div>
                </div>
        `);
    }
}

function close_modal() {
    $("#hint").hide();
    $("#get").hide();
    $("#paragraphs").empty();
    selected_paragraphs.clear();
}

var selected_paragraphs = new Set();
var selected_document = "";

function select_paragraph(id) {
    if ($("#bar" + id).css("background-color") == "rgb(76, 175, 80)") {
        selected_paragraphs.delete(id);
        $("#bar" + id).css("background-color", "#aaaaaa");
    } else {
        selected_paragraphs.add(id);
        $("#bar" + id).css("background-color", "#4caf50");
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

    if (!all_correct) {
        alert("Выбирать можно только последовательно идущие абзацы!");
    } else {
        $.ajax({
                url: "../api/test_script.txt",
                method: "POST",
                data: {
                    id: user_id
                },
                dataType: "json"
            })
            .done(function(data) {
                /**/
            })
            .fail(function(jqXHR, status) {
                close_modal();
                var id = 12;
                edit_block(id);
            });
    }
}

function select_document(id) {
    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            $("#hint").show();
            $("#get").show();
            $("#paragraphs").empty();
            selected_paragraphs.clear();

            selected_document = id;
            $("#get").click(create_block);

            var text = [{
                text: `I am a very simple card. I am good at containing small bits of information.`,
                status: 0
            }, {
                text: `I am a very simple card. I am good at containing small bits of information.`,
                status: 0
            }, {
                text: `I am convenient because I require little markup to use effectively.I am a very simple card. I am good at containing small bits of information.`,
                status: 1
            }, {
                text: `I am convenient because`,
                status: 0
            }, {
                text: `I am convenient because`,
                status: 0
            }];

            for (var i = 0; i < text.length; ++i) {
                var id = i;

                $("#paragraphs").append(`
                <div class="row paragraphs-flex" id="p` + id + `" ` + (text[i].status == 0 ? `onclick="select_paragraph(` + id + `);"` : ``) + `>
                    <div class="col s1">
                        <div style="background: ` + (text[i].status == 0 ? "#aaa" : "#fa0000") + ` !important;" class="indicator" id="bar` + id + `"></div>
                    </div>
                    <div class="col s11">
                        <p class="slim">
                        &nbsp;&nbsp;&nbsp;&nbsp;` + text[i].text + `
                        </p>
                    </div>
                </div>
                `);
            }
        });
}

function list_documents(lang) {
    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            $("#hint").hide();
            $("#get").hide();
            $("#paragraphs").empty();
            $("#docs").empty();
            for (var i = 0; i < 7; ++i) {
                var id = i;
                var tags = ["Английский", "Дезинфекция", "Массачусетс", "Городские мероприятия"];
                var title = "«" + "Disinfection instructions" + "»";
                var ready = 20;
                var total = 55;
                var progress = ((ready / total) * 100).toFixed(1) + "%";

                var tags_markup = "";
                for (var j = 0; j < tags.length; ++j) {
                    tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                }

                $("#docs").append(`
                    <li class="collection-item avatar" onclick="select_document(` + id + `);">
                    <i class="material-icons circle">schedule</i>
                    <p>
                    ` + title + `
                    </p>
                    <div class="progress-bg"></div>
                    <div class="progress-ind" style="width: ` + progress + `;"></div>
                    <div class="tags-par">
                    ` + tags_markup + `
                    </div>
                    </li>
                `);
            }
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

    $.ajax({
            url: "../api/test_script.txt",
            method: "POST",
            data: {
                id: user_id
            },
            dataType: "json"
        })
        .done(function(data) {
            /**/
        })
        .fail(function(jqXHR, status) {
            list_blocks();
        });
}

$(document).ready(function() {
    check_user(init);
});