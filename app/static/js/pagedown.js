var f = function(textid, previewid) {
    if (typeof flask_pagedown_converter === "undefined")
        flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
    log('textid',textid)
    log('previewid',previewid)
    var textarea = qs(textid);
    var preview = qs(previewid);
    textarea.onkeyup = function() { 
        preview.innerHTML = flask_pagedown_converter(textarea.value); 
    }

    textarea.onkeyup.call(textarea);
}

var loadPostPagedownPreview = function(textid, previewid) {
    f(textid, previewid)
}

var _main_pagedown = function() {
    loadPostPagedownPreview('#flask-pagedown-body', '#flask-pagedown-body-preview')
}


$( document ).ready(function(){
    _main_pagedown()
})