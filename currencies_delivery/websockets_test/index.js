var initWebsockets = function (url) {
    return new WebSocketConnectionHandler(url);
};

$(document).ready(function () {
    var ws = initWebsockets("localhost:8080/currencies/");

    ws.on('authorized', function () {
        console.log('authorized');
    });

    ws.emit('authorize', {token: '7cb14636254343b210f00901392c22ea7beabf15'});

    ws.on('client error', function (data) {
        console.log('Client error:', data);
    });

    ws.emit('subscribe');

    ws.on('new values', function (data) {
        console.log(data);
    });

});
