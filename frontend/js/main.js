$(document).ready(function() {
    $('.modal').modal();
    $('select').formSelect();
});

function select_paragraph(id) {
    if ($("#bar" + id).css("background-color") == "rgb(76, 175, 80)") {
        $("#bar" + id).css("background-color", "#aaaaaa");
    } else {
        $("#bar" + id).css("background-color", "#4caf50");
    }
}