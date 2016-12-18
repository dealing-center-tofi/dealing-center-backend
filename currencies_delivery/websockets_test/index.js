var initWebsockets = function (url) {
    return new WebSocketConnectionHandler(url);
};

$(document).ready(function () {
    var ws = initWebsockets("dealing-center.westeurope.cloudapp.azure.com/websocket/currencies/");

    ws.on('authorized', function () {
        console.log('authorized');
    });

    ws.emit('authorize', {token: 'Insert token here...'});

    ws.on('client error', function (data) {
        console.log('Client error:', data);
    });

    ws.emit('subscribe');

    ws.emit('orders_closing_subscribe');

    ws.on('new values', function (data) {
        console.log(data);
    });

    ws.on('order closed', function (data) {
        console.log(data);
    });

});
