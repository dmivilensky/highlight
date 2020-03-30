var user_id = "";
var block_id = "";

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

function back() {
    $.redirectGet("main.html", {
        user_id: user_id
    });
}

function ready(id) {
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
            location.reload(true);
        });
}

function save(id) {
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
            location.reload(true);
        });
}

function init() {
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
            var text = [
                `I am a very simple card. I am good at containing small bits of information.`,
                `I am convenient because I require little markup to use effectively.I am a very simple card. I am good at containing small bits of information.`,
                `I am convenient because`
            ];
            var translate = [
                `FFF I am a very simple card. I am good at containing small bits of information.`,
                `ormation.`,
                `I am convenient because`
            ];
            var status = [
                0,
                0,
                1
            ];

            for (var i = 0; i < text.length; ++i) {
                var id = i;

                var translation_markup = "";
                if (status[i] == 0) {
                    translation_markup = `
                    <form class="col s12" style="background: #eee; border-radius: 5px;">
                    <div class="row" style="margin: 0;">
                        <div class="input-field col s12" style="margin: 0;">
                        <textarea placeholder="Перевод" id="textarea` + id + `" class="materialize-textarea" style="height: 200px;">` + translate[i] + `</textarea>
                        </div>
                    </div>
                    </form>
                    `;
                } else {
                    translation_markup = `
                    <p>
                        &nbsp;&nbsp;&nbsp;&nbsp;` + translate[i] + `
                    </p>`;
                }

                $("#translations").append(`
                <div class="col s12 m12">
                <div class="card">
                    <div class="card-content">
                    <div class="row">
                        <div class="col s12 m6 l6">
                            <p>
                            &nbsp;&nbsp;&nbsp;&nbsp;` + text[i] + `
                            </p>
                        </div>

                        <div class="col s12 m6 l6">
                            ` + translation_markup + `
                        </div>
                    </div> 
                    </div>

                    <div style="width: 100%; text-align: right; padding: 20px; padding-top:0;">
                        <a onclick="ready(` + id + `);" class="waves-effect waves-light btn yellow darken-2">Перевод завершён</a>
                        <a onclick="save(` + id + `);" class="waves-effect waves-light btn green">Сохранить</a>
                    </div>
                </div>
                </div>
                `);
            }
        });
}

$(document).ready(function() {
    check_user(init);
});