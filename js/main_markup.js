var user_id = "";

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
            alert('Ошибка сервера!');
            $.redirectGet("index.html", {});
        });
}

var doc_id;

async function corrected() {
    var extention = $("#corrections_path").val().split('.').pop()
    if (extention != "docx" && extention != "pdf") {
        alert("Необходимо загрузить исправленный .docx или .pdf файл!");
    } else {
        var fname = 'new_file' + getRandomInt(10000) + '.' + extention;
        $("#corrections_path").val(fname);

        $('#file').on('submit', function(event) {
            // event.preventDefault();

            var post_data = new FormData($("#file")[0]);
            post_data.append("id", user_id);
            post_data.append("document_id", doc_id);

            $.ajax({
                xhr: function() {
                    var xhr = new window.XMLHttpRequest();

                    xhr.upload.addEventListener("progress", function(evt) {
                        var percent = Math.round(evt.loaded / evt.total * 100);
                        $('#submitting_button').attr('disabled', true);
                        $('#submitting_button').get(0).innerText = "Загружено: " + percent + '%'
                    }, false);

                    xhr.upload.addEventListener("load", function(evt) {
                        $('#submitting_button').css('background-color', 'green').delay(2000);
                        $('#submitting_button').get(0).innerText = "Готово, ждём ответа сервера..."

                    }, false);

                    return xhr;
                },
                url: "/api/markup_file",
                type: "POST",
                data: post_data,
                processData: false,
                contentType: false,
                success: function(result) {
                    $('#submitting_button').attr('disabled', false);
                    alert("Файл загружен!");
                    $('#submitting_button').get(0).innerText = "ЗАГРУЗИТЬ ФАЙЛ";
                }
            });
        });
        $("#file").submit();
    }

}

var title = "";
var translation = "";

var documents;

function document_info(i) {
    $("#details").empty();

    doc_id = documents[i]._id;

    title = "«" + documents[i].name + "»";
    var tags = documents[i].tags.split(",");
    var tags_markup = "";
    for (var j = 0; j < tags.length; ++j) {
        tags_markup += `<div class="chip">` + tags[j] + `</div>`;
    }

    var original = documents[i].orig_path;
    var original_text = "";
    if (original) {
        var or_s = original.split('/');
        original_text = `
        <div class="col s6">
        <a href="files/` + or_s[or_s.length - 1] + `" target="_blank" class="waves-effect waves-green btn-flat download-btns ready-btn"><i class="material-icons left">get_app</i>Скачать оригинал</a>
        </div>
        `;
    }

    translation = documents[i].path;
    var translation_text = "";
    if (translation) {
        var tr_s = translation.split('/');
        translation_text = `
        <div class="col s6">
        <a href="files/` + tr_s[tr_s.length - 1] + `" target="_blank" class="waves-effect waves-light btn green download-btns"><i class="material-icons left">get_app</i>Скачать перевод</a>
        </div>
        `;
    }

    $("#details").append(`
    <li class="collection-item avatar">
        <i class="material-icons circle yellow darken-2">find_in_page</i>
        <span class="title">` + title + `</span>
        
        <div class="tags-block">
        ` + tags_markup + `
        </div>
        
        <div class="row editor-buttons">
            ` + translation_text + `
            ` + original_text + `
        </div>
        <div class="row">
            <div class="col s6">
            <a class="waves-effect waves-light btn grey modal-trigger download-translation" href="#modal1"><i class="material-icons left">send</i>Исправления</a>
            </div>
        </div>
    </li>
    `);
}

function update_search() {
    var tags_list = "";
    var tags_data = M.Chips.getInstance($('#tags_edit')).chipsData;
    for (var i = 0; i < tags_data.length; ++i) {
        tags_list += tags_data[i].tag + ",";
    }
    tags_list = tags_list.slice(0, -1);
    $('#loader_docs').show();
    $('#text_docs').hide();

    $.ajax({
            url: "api/get_from_db_for_verst",
            method: "POST",
            data: {
                search: $('#search').val(),
                tags: tags_list
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            $('#loader_docs').hide();
            if (response.code == "OK") {
                $("#docs").empty();
                $("#details").empty();

                documents = response.document;
                if (documents.length == 0) {
                    $('#text_docs').show();
                }
                for (var i = 0; i < documents.length; ++i) {
                    var tags = documents[i].tags.split(",");
                    var title = "«" + documents[i].name + "»";

                    var tags_markup = "";
                    for (var j = 0; j < tags.length; ++j) {
                        tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                    }

                    $("#docs").append(`
                    <li class="collection-item avatar" onclick="document_info(` + i + `);">
                        <i class="material-icons circle yellow darken-2">find_in_page</i>
                        <span class="title"><a>` + title + `</a></span>
                        <div class="docs-tags">
                        ` + tags_markup + `
                        </div>
                    </li>
                    `);
                }
            } else {
                $('#text_docs').show();
            }
        })
        .fail(function(jqXHR, status, error) {
            $("#docs").empty();
            $("#details").empty();
            $('#loader_docs').hide();
            alert('Ошибка сервера!');
        });
}

function init() {
    $('.tooltipped').tooltip();
    $('.modal').modal();
    $('.chips-placeholder').chips({
        placeholder: 'Enter a tag',
        secondaryPlaceholder: '+Tag',
        onChipAdd: function(e, chip) {
            update_search();
        },
    });

    $('#search').keypress(function(event) {
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if (keycode == '13') {
            update_search();
        }
    });

    update_search();
}

$(document).ready(function() {
    csrf_setup();
    check_user(init);
});