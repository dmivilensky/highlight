function inc_importance(i, id_) {
    //csrf_setup();
    $.ajax({
            url: "api/update_importance",
            method: "POST",
            data: {
                id: id_
            },
            dataType: "json"
        })
        .done(function(data) {
            response = data;
            if (response.code == "OK") {
                document_info(i);
                alert("Теперь этот файл будет иметь больший вес при переводе. Спасибо!")
            }
        })
        .fail(function(jqXHR, status, error) {
            alert('Ошибка сервера!');
        });
}

var title = "";
var translation = "";
var original = "";

function send_file() {
    //csrf_setup();
    var email = $("#email").val();
    var fpath = $("#translated_d").is(':checked') ? translation : original;
    $.ajax({
            url: "api/send_email",
            method: "POST",
            data: {
                name: title,
                email: email,
                path: fpath
            },
            dataType: "text"
        })
        .done(function(data) {
            alert("Файл будет отправлен на указанную почту");
        })
        .fail(function(jqXHR, status, error) {
            alert("Ошибка соединения с сервером. Попробуйте зайти позднее.")
        });
}

var documents;

function document_info(i) {
    $("#details").empty();
    title = "«" + documents[i].name + "»";
    var tags = documents[i].tags.split(",");
    var tags_markup = "";
    for (var j = 0; j < tags.length; ++j) {
        tags_markup += `<div class="chip">` + tags[j] + `</div>`;
    }

    original = documents[i].orig_path;
    var original_text = "";
    if (original) {
        var or_s = original.split("/");
        original_text = `
        <div class="col s6">
        <a href="` + (or_s[0] != "http:" && or_s[0] != "https:" ? "files/" + (or_s.length < 2 || or_s[or_s.length - 2] == "files" ? or_s[or_s.length - 1] : or_s.slice(or_s.indexOf("files") + 1, or_s.length).join("/")) : original) + `" target="_blank" class="waves-effect waves-green btn-flat download-btns ready-btn"><i class="material-icons left">get_app</i>Скачать оригинал</a>
        </div>
        `;
    }

    if (documents[i].path == null)
        $("#translated_d").attr('disabled', true);
    translation = documents[i].path;
    var translation_text = "";
    if (translation) {
        var tr_s = translation.split("/");
        translation_text = `
        <div class="col s6">
        <a href="` + (tr_s[0] != "http:" && tr_s[0] != "https:" ? "files/" + (tr_s.length < 2 || tr_s[tr_s.length - 2] == "files" ? tr_s[tr_s.length - 1] : tr_s.slice(tr_s.indexOf("files") + 1, tr_s.length).join("/")) : translation) + `" target="_blank" class="waves-effect waves-light btn green download-btns"><i class="material-icons left">get_app</i>Скачать перевод</a>
        </div>
        `;
    }

    var status = documents[i].status;
    var avatar = "";
    var status_text = "";
    var importance_text = "";
    if (status == 'TRANSLATED') {
        avatar = `<i class="material-icons circle green">spellcheck</i>`;
        status_text = `Переведён и проверен`;
    } else if (status == 'NEED_CHECK') {
        avatar = `<i class="material-icons circle yellow darken-2">find_in_page</i>`;
        status_text = `Переведён`;
    } else {
        avatar = `<i class="material-icons circle">schedule</i>`;
        status_text = `В работе`;
    }
    importance_text = `<a onclick="inc_importance(` + i + `, '` + documents[i]._id + `');" class="secondary-content tooltipped" data-position="left" data-tooltip="Очень нужно!"><i class="material-icons grey-star">star_border</i></a>`;

    $("#details").append(`
    <li class="collection-item avatar">
        ` + avatar + `
        <span class="title status-text">` + status_text + `</span><br>
        <span class="title">` + title + `</span>
        ` + importance_text + `
        <div class="tags-block">
        ` + tags_markup + `
        </div>
        
        <div class="row btns">
            ` + translation_text + `
            ` + original_text + `
        </div>
        <div class="row">
            <div class="col s12">
            <a class="waves-effect waves-light btn grey modal-trigger send-file" href="#modal1"><i class="material-icons left">send</i>Отправить на почту</a>
            </div>
        </div>
    </li>
    `);
}

function previous_page() {
    $('#page').text($('#page').text() >= 2 ? (parseInt($('#page').text())-1) : 1);
    update_search()
}

function next_page() {
    $('#page').text(parseInt($('#page').text())+1);
    update_search()
}

function update_search() {
    var tags_list = "";
    var tags_data = M.Chips.getInstance($('#tags')).chipsData;
    for (var i = 0; i < tags_data.length; ++i) {
        tags_list += tags_data[i].tag + ",";
    }
    tags_list = tags_list.slice(0, -1);
    $('#loader_docs').show();
    $('#text_docs').hide();
    var page = $('#page').text();
    page = parseInt(page) - 1;

    //csrf_setup();

    $.ajax({
            url: "api/get_from_db",
            method: "POST",
            data: {
                search: $('#search').val(),
                tags: tags_list,
                page: page
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
                    var status = documents[i].status;

                    var tags = documents[i].tags.split(",");
                    var title = "«" + documents[i].name + "»";

                    var tags_markup = "";
                    for (var j = 0; j < tags.length; ++j) {
                        tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                    }

                    var avatar = "";
                    if (status == 'TRANSLATED') {
                        avatar = `<i class="material-icons circle green">spellcheck</i>`;
                    } else if (status == 'NEED_CHECK') {
                        avatar = `<i class="material-icons circle yellow darken-2">find_in_page</i>`;
                    } else {
                        avatar = `<i class="material-icons circle">schedule</i>`;
                    }

                    $("#docs").append(`
                        <li class="collection-item avatar" onclick="document_info(` + i + `);">
                            ` + avatar + `
                            <span class="title"><a>` + title + `</a></span>
                            <div class="tags-mu">
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
            alert('Ошибка сервера!');
            $("#docs").empty();
            $("#details").empty();
            $('#loader_docs').hide();
        });
}

$(document).ready(function() {
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
});