function signin() {
    if ($('#editor').is(':checked')) {
        window.location.href = 'main_editor.html';
    } else {
        window.location.href = 'main.html';
    }
}