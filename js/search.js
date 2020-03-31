function inc_importance(id) {
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
            document_info(id);
            alert("Теперь этот файл будет иметь больший вес при переводе. Спасибо!")
        });
}

var title = "";
var translation = "";

function send_file() {
    var email = $("#email").val();
}

function document_info(id) {
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
            $("#details").empty();

            title = "«" + "Disinfection instructions" + "»";
            var tags = ["Английский", "Дезинфекция", "Массачусетс", "Городские мероприятия"];
            var tags_markup = "";
            for (var j = 0; j < tags.length; ++j) {
                tags_markup += `<div class="chip">` + tags[j] + `</div>`;
            }

            var original = "privacy_policy.pdf";
            translation = "privacy_policy.pdf";

            var status = 2;
            var avatar = "";
            var status_text = "";
            if (status == 2) {
                avatar = `<i class="material-icons circle green">spellcheck</i>`;
                status_text = `Переведён и проверен`;
            } else if (status == 1) {
                avatar = `<i class="material-icons circle yellow darken-2">find_in_page</i>`;
                status_text = `Переведён`;
            } else {
                avatar = `<i class="material-icons circle">schedule</i>`;
                status_text = `В работе`;
            }

            $("#details").append(`
            <li class="collection-item avatar">
                ` + avatar + `
                <span class="title" style="font-size: 12px; font-family: Consolas, monaco, monospace;">` + status_text + `</span><br>
                <span class="title">` + title + `</span>
                
                <a onclick="inc_importance(` + id + `);" class="secondary-content tooltipped" data-position="left" data-tooltip="Очень нужно!"><i class="material-icons" style="color: #444;">star_border</i></a>
        
                <div style="margin-top: 10px;padding-right: 10%;">
                ` + tags_markup + `
                </div>
        
                <div class="row" style="margin-top: 20px;">
                    <div class="col s6">
                    <a href="` + translation + `" class="waves-effect waves-light btn green" style="width: 100%; border-radius: 20px;"><i class="material-icons left">get_app</i>Скачать перевод</a>
                    </div>
                    <div class="col s6">
                    <a href="` + original + `" class="waves-effect waves-green btn-flat" style="width: 100%; border-radius: 20px; text-align: center;"><i class="material-icons left">get_app</i>Скачать оригинал</a>
                    </div>
                </div>
                <div class="row">
                    <div class="col s6">
                    <a class="waves-effect waves-light btn grey modal-trigger" style="width: 100%; border-radius: 20px;" href="#modal1"><i class="material-icons left">send</i>Отправить на почту</a>
                    </div>
                </div>
            </li>
            `);
        });
}

function update_search() {
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
            $("#docs").empty();
            $("#details").empty();

            var status = [2, 2, 2, 1, 1, 1, 0]

            for (var i = 0; i < 7; ++i) {
                var id = i;
                var tags = ["Английский", "Дезинфекция", "Массачусетс", "Городские мероприятия"];
                var title = "«" + "Disinfection instructions" + "»";

                var tags_markup = "";
                for (var j = 0; j < tags.length; ++j) {
                    tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                }

                var avatar = "";
                if (status[i] == 2) {
                    avatar = `<i class="material-icons circle green">spellcheck</i>`;
                } else if (status[i] == 1) {
                    avatar = `<i class="material-icons circle yellow darken-2">find_in_page</i>`;
                } else {
                    avatar = `<i class="material-icons circle">schedule</i>`;
                }

                $("#docs").append(`
                    <li class="collection-item avatar" onclick="document_info(` + id + `);">
                        ` + avatar + `
                        <span class="title"><a href="">` + title + `</a></span>
                        <div style="margin-top: 10px;padding-right: 10%;">
                        ` + tags_markup + `
                        </div>
                    </li>
            `);
            }
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