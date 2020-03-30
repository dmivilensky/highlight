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
            alert("success");
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
        var data_text = new Blob(["<html><body>" + text.join("\n\n") + "</body></html>"], { type: 'text/plain' });
        var url_text = window.URL.createObjectURL(data_text);

        var translate = [
            `FFF I am a very simple card. I am good at containing small bits of information.`,
            `I am convenient because I require little markup to use effectively.I am a very simple card. I am good at containing small bits of information.`,
            `I am convenient because`
        ];
        var data_translate = new Blob(["<html><body>" + translate.join("\n\n") + "</body></html>"], { type: 'text/plain' });
        var url_translate = window.URL.createObjectURL(data_translate);

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
                        
                        <div style="margin-top: 10px; margin-bottom: 10px; padding-right: 10%;">
                        ` + tags_markup + `
                        </div>
                        <div style="width: 100%; margin-bottom: 10px;">
                        <a href="` + url_text + `" download="original.txt" class="waves-effect waves-light btn green" style="width: 100%; border-radius: 20px;"><i class="material-icons left">file_download</i>Скачать отрывок</a>
                        </div>
                        <div style="width: 100%; margin-bottom: 10px;">
                        <a href="` + url_translate + `" download="translate.txt" class="waves-effect waves-green btn-flat" style="width: 100%; text-align: center; border-radius: 20px;"><i class="material-icons left">file_download</i>Скачать текущий перевод</a>
                        </div>
                        <p class="preview">` + text[0].slice(0, 150) + `</p>
                        </div>
                        <div class="card-action" style="text-align: right;">
                        <a onclick="edit_block(` + id + `);" style="color: #4caf50;">Продолжить перевод</a>
                        </div>
                    </div>
                </div>
        `);
    }
}

function init() {
    $('.modal').modal();
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
            alert("success");
        })
        .fail(function(jqXHR, status) {
            list_blocks();
        });
}

function select_paragraph(id) {
    if ($("#bar" + id).css("background-color") == "rgb(76, 175, 80)") {
        $("#bar" + id).css("background-color", "#aaaaaa");
    } else {
        $("#bar" + id).css("background-color", "#4caf50");
    }
}

$(document).ready(function() {
    check_user(init);
});