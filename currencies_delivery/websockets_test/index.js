var initWebsockets = function (url) {
    return new WebSocketConnectionHandler(url);
};

$(document).ready(function () {
    var ws = initWebsockets("localhost:8080/currencies/");

    ws.on('event', function (data) {
        console.log('received:', data);
    });

    ws.on('client error', function (data) {
        console.log('Client error:', data);
    });

    ws.emit('connect');
    ws.emit('event', {s: 1, e: 2});
    ws.emit('event', {s: 1, e: 3});
    ws.emit('event', {s: 2, e: 3});

});
