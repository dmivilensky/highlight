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

function downloadURI(uri, name) {
    var link = document.createElement("a");
    link.download = name;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    delete link;
}

function text_uri(text) {
    var text_data = new Blob(["\ufeff" + text], { type: 'text/plain; charset=utf-8' });
    return window.URL.createObjectURL(text_data);
}

function download_text(text, file) {
    downloadURI(text_uri(text), file);
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function load_pdf_pages(path, canvas_id, scale) {
    var loadingTask = pdfjsLib.getDocument(path);
    loadingTask.promise.then(function(pdf) {
        pdf.getPage(1).then(function(page) {
            var viewport = page.getViewport({ scale: scale, });

            var canvas = document.getElementById(canvas_id);
            var context = canvas.getContext('2d');
            canvas.height = viewport.height;
            canvas.width = viewport.width;

            var renderContext = {
                canvasContext: context,
                viewport: viewport
            };
            page.render(renderContext);
        });
    });
}