function autoResize(id) {
    var i = document.getElementById(id);
    var iframeHeight = i.contentWindow.document.body.scrollHeight;
    i.height=iframeHeight;
}
