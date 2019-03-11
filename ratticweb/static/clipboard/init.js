/* JS clipboard init */  
var passwd_clipboard = new ClipboardJS('#js-copy-passwd');
var name_clipboard = new ClipboardJS('#js-copy-name');

name_clipboard.on('success', function (e) {
    e.clearSelection();
});

// dirty hacks with dirty hacks
passwd_clipboard.on('success', function (e) {
    e.clearSelection();
    $('#password').trigger('getdata')
    setTimeout(function() {
        e.clearSelection();
        $('#js-copy-passwd').click()
    }, 1000)
    setTimeout(function () {
        e.clearSelection();
    }, 1000)
});

