$(document).ready(function() {
    $('.tooltipped').tooltip();
    $('.modal').modal();
    $('.chips-placeholder').chips({
        placeholder: 'Enter a tag',
        secondaryPlaceholder: '+Tag',
    });
});