var WebSocketConnectionHandler = function (url) {
    var self = this;

    this.events = {};
    this.ws = new WebSocket("ws://" + url);
    this.opened = false;

    this.ws.onopen = function() {
        console.log('connected');
        self.opened = true;
    };

    this.ws.onclose = function(e) {
        self.opened = false;
    };

    this.getEventParams = function (data) {
        var eventName = data.splice(0, 1)[0];
        return {
            eventName: eventName,
            data: data
        };
    };

    this.ws.onmessage = function(e) {
        var data = JSON.parse(e.data);
        var eventParams = self.getEventParams(data);
        self.events[eventParams.eventName].apply(self, eventParams.data);
    };
};

WebSocketConnectionHandler.prototype.on = function(event, fn) {
    this.events[event] = fn;
};

WebSocketConnectionHandler.prototype.emit = function(event, data) {
    var message = JSON.stringify([event, data]);
    if (this.opened) {
        this.ws.send(message);
    } else {
        var that = this;
        setTimeout(function () {that.emit(event, data)}, 100);
    }
};
