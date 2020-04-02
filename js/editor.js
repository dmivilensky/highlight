var user_id = "";
var block_id = "";

function check_user(success) {
    user_id = findGetParameter("user_id");
    block_id = findGetParameter("block_id");

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

function back() {
    $.redirectGet("main.html", {
        user_id: user_id
    });
}

var piece;

function ready(i) {
    piece.translated_txt[i] = $("#textarea" + i).val();

    $.ajax({
            url: "api/update_translating_pieces",
            method: "POST",
            data: {
                id: user_id,
                piece_id: block_id,
                txt: piece.translated_txt.join("#del#")
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            response = data;
            if (response.code == "OK") {
                location.reload(true);
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

function save() {
    for (var i = 0; i < piece.translated_txt.length; ++i) {
        piece.translated_txt[i] = $("#textarea" + i).val();
    }

    $.ajax({
            url: "api/update_translating_pieces",
            method: "POST",
            data: {
                id: user_id,
                piece_id: block_id,
                txt: piece.translated_txt.join("#del#"),
                status: "DONE"
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            response = data;
            if (response.code == "OK") {
                $.redirectGet("main.index", {
                    user_id: id
                });
            }
        })
        .fail(function(jqXHR, status, error) {
            console.log(error);
        });
}

function init() {
    $.ajax({
            url: "api/find_piece",
            method: "POST",
            data: {
                id: user_id,
                piece_id: block_id
            },
            dataType: "json"
        })
        .done(function(data) {
            console.log(data);
            response = data;
            if (response.code == "OK") {
                piece = response.document;

                if (!piece.translated_txt) {
                    piece.translated_txt = [];
                    for (var i = 0; i < piece.txt.length; ++i) {
                        piece.translated_txt.push("");
                    }
                }
                for (var i = 0; i < piece.txt.length; ++i) {
                    var translation_markup = "";

                    if (piece.translation_status == 'UNDONE') {
                        translation_markup = `
                        <form class="col s12 translation-block">
                        <div class="row slim">
                            <div class="input-field col s12 slim">
                            <textarea placeholder="Перевод" id="textarea` + i + `" class="materialize-textarea translation-edit">` + piece.translated_txt[i] + `</textarea>
                            </div>
                        </div>
                        </form>
                        `;
                    } else {
                        translation_markup = `
                        <p>
                            &nbsp;&nbsp;&nbsp;&nbsp;` + piece.translated_txt[i] + `
                        </p>`;
                    }

                    $("#translations").append(`
                    <div class="col s12 m12">
                    <div class="card">
                        <div class="card-content">
                        <div class="row">
                            <div class="col s12 m6 l6">
                                <p>
                                &nbsp;&nbsp;&nbsp;&nbsp;` + piece.txt[i] + `
                                </p>
                            </div>
    
                            <div class="col s12 m6 l6">
                                ` + translation_markup + `
                            </div>
                        </div> 
                        </div>
    
                        <div class="translation-buttons">
                            <a onclick="ready(` + i + `);" class="waves-effect waves-light btn yellow darken-2">Сохранить</a>
                        </div>
                    </div>
                    </div>
                    `);
                }
            }
        })
        .fail(function(jqXHR, status) {});
}

$(document).ready(function() {
    check_user(init);
});