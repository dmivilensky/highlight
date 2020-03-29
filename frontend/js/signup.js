$(document).ready(function() {
    $('select').formSelect();
});

var social_idx = 1;

function add_social() {
    $('#soc').append(`
        <div class="input-field col s12 m12 l4">
            <select id="soc_value` + social_idx + `" style="margin-top: 15px;">
            <option value="1" selected>ВК</option>
            <option value="2">Facebook</option>
            <option value="3">Telegram</option>
            </select>
            <label>Соц. сеть</label>
        </div>

        <div class="input-field col s12 m12 l8">
            <input id="soc` + social_idx + `" type="text" class="validate">
            <label for="soc` + social_idx + `">id</label>
        </div>
    `);
    $('select').formSelect();
    ++social_idx;
}