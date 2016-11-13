from websocket_app.handlers import WebSocketHandler


class CurrencyDeliveryHandler(WebSocketHandler):
    def __init__(self, application, request, app_name, room_controller, api_helper, **kwargs):
        super(CurrencyDeliveryHandler, self).__init__(application, request, app_name, **kwargs)
        self.room_ctrl = room_controller
        self.api = api_helper

    def on_close(self):
        super(CurrencyDeliveryHandler, self).on_close()
        self.room_ctrl.leave_rooms_for_client(self)

    def register_events(self):
        self.events_handlers = {
            'event': self.just_event,
            'connect': self.connect_room
        }

    def just_event(self, data):
        self.broadcast_to('name', 'event', data)

    def connect_room(self, data):
        self.room_ctrl.join_room('name', self)
