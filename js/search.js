function inc_importance(id_) {
    $.ajax({
            url: "api/update_importance",
            method: "POST",
            data: {
                id: id_
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            response = data;
            if (response.code == "OK") {
                document_info(id);
                alert("Теперь этот файл будет иметь больший вес при переводе. Спасибо!")
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

var title = "";
var translation = "";

function send_file() {
    var email = $("#email").val();
    $.ajax({
            url: "../php_scripts/send_mail.php",
            method: "GET",
            data: {
                name: title,
                email: email,
                path: translation
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

    var original = documents[i].orig_path;
    var original_text = "";
    if (original) {
        original_text = `
        <div class="col s6">
        <a href="` + original + `" target="_blank" class="waves-effect waves-green btn-flat download-btns"><i class="material-icons left">get_app</i>Скачать оригинал</a>
        </div>
        `;
    }

    translation = documents[i].path;
    var translation_text = "";
    if (translation) {
        translation_text = `
        <div class="col s6">
        <a href="` + translation + `" target="_blank" class="waves-effect waves-light btn green download-btns"><i class="material-icons left">get_app</i>Скачать перевод</a>
        </div>
        `;
    }

    var status = documents[i].status;
    var avatar = "";
    var status_text = "";
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

    $("#details").append(`
    <li class="collection-item avatar">
        ` + avatar + `
        <span class="title status-text">` + status_text + `</span><br>
        <span class="title">` + title + `</span>
                
        <a onclick="inc_importance(` + documents[i]._id + `);" class="secondary-content tooltipped" data-position="left" data-tooltip="Очень нужно!"><i class="material-icons grey-star">star_border</i></a>
        
        <div class="tags-block">
        ` + tags_markup + `
        </div>
        
        <div class="row btns">
            ` + translation_text + `
            ` + original_text + `
        </div>
        <div class="row">
            <div class="col s6">
            <a class="waves-effect waves-light btn grey modal-trigger send-file" href="#modal1"><i class="material-icons left">send</i>Отправить на почту</a>
            </div>
        </div>
    </li>
    `);
}

function update_search() {
    var tags_list = "";
    var tags_data = M.Chips.getInstance($('#tags')).chipsData;
    for (var i = 0; i < tags_data.length; ++i) {
        tags_list += tags_data[i].tag + ",";
    }
    tags_list = tags_list.slice(0, -1);

    $.ajax({
            url: "api/get_from_db",
            method: "POST",
            data: {
                search: $('#search').val(),
                tags: tags_list
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            response = data;
            if (response.code == "OK") {
                $("#docs").empty();
                $("#details").empty();

                documents = response.document;
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
                            <span class="title"><a href="">` + title + `</a></span>
                            <div class="tags-mu">
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
});