var user_id = "";

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

function corrected() {
    var extention = $("#corrections_path").val().slice(-4, -1) + $("#corrections_path").val().slice(-1);
    if (extention != "docx") {
        alert("Необходимо загрузить исправленный .docx файл!");
    } else {
        $("#corrections_path").val('new_file' + getRandomInt(10000) + '.docx');
        $("#file").submit();

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
                /**/
            });
    }
}

var title = "";
var translation = "";

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

            $("#details").append(`
            <li class="collection-item avatar">
                <i class="material-icons circle yellow darken-2">find_in_page</i>
                <span class="title">` + title + `</span>
        
                <div class="tags-block">
                ` + tags_markup + `
                </div>
        
                <div class="row editor-buttons">
                    <div class="col s6">
                    <a href="` + translation + `" target="_blank" class="waves-effect waves-light btn green download-translation"><i class="material-icons left">get_app</i>Скачать перевод</a>
                    </div>
                    <div class="col s6">
                    <a href="` + original + `" target="_blank" class="waves-effect waves-green btn-flat download-original"><i class="material-icons left">get_app</i>Скачать оригинал</a>
                    </div>
                </div>
                <div class="row">
                    <div class="col s6">
                    <a class="waves-effect waves-light btn grey modal-trigger download-translation" href="#modal1"><i class="material-icons left">send</i>Исправления</a>
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

            for (var i = 0; i < 7; ++i) {
                var id = i;
                var tags = ["Английский", "Дезинфекция", "Массачусетс", "Городские мероприятия"];
                var title = "«" + "Disinfection instructions" + "»";

                var tags_markup = "";
                for (var j = 0; j < tags.length; ++j) {
                    tags_markup += `<div class="chip">` + tags[j] + `</div>`;
                }

                $("#docs").append(`
                    <li class="collection-item avatar" onclick="document_info(` + id + `);">
                        <i class="material-icons circle yellow darken-2">find_in_page</i>
                        <span class="title"><a href="">` + title + `</a></span>
                        <div class="docs-tags">
                        ` + tags_markup + `
                        </div>
                    </li>
            `);
            }
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
}

$(document).ready(function() {
    check_user(init);
});