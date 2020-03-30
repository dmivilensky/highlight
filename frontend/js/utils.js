function getRandomInt(max) {
    return Math.floor(Math.random() * Math.floor(max));
}

$.extend({
    redirectPost: function(location, args) {
        var form = '';
        $.each(args, function(key, value) {
            form += '<input type="hidden" name="' + key + '" value="' + value + '">';
        });
        var id = getRandomInt(1000000);
        var form_markup = '<form action="' + location + '" method="POST" id="' + id + '">' + form + '</form>';
        $(document.body).append(form_markup);
        $("#" + id).submit();
    }
});

$.extend({
    redirectGet: function(location, args) {
        var form = '';
        $.each(args, function(key, value) {
            form += '<input type="hidden" name="' + key + '" value="' + value + '">';
        });
        var id = getRandomInt(1000000);
        var form_markup = '<form action="' + location + '" method="GET" id="' + id + '">' + form + '</form>';
        $(document.body).append(form_markup);
        $("#" + id).submit();
    }
});

hashCode = function(s) {
    var content = "" + s;
    var h = 0,
        l = content.length,
        i = 0;
    if (l > 0) {
        while (i < l) {
            h = (h << 5) - h + content.charCodeAt(i++) | 0;
        }
    }
    return h;
};

function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function(item) {
            tmp = item.split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}