import logging

from websocket_app.handlers import WebSocketHandler


access_log = logging.getLogger("tornado.access")


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
            'authorize': self.authorize,
            'subscribe': self.subscribe,
            'unsubscribe': self.unsubscribe
        }

    def authorize(self, data):
        self.api.headers.update({'Authorization': 'Token %s' % data['token']})
        response = self.api.do_request('GET', '/users/me/')
        if response.status_code == 200:
            self.emit('authorized')
        else:
            pass

    def subscribe(self, data):
        access_log.log(logging.DEBUG, 'subscribed: %s' % self)
        self.room_ctrl.join_room('delivery', self)

    def unsubscribe(self, data):
        access_log.log(logging.DEBUG, 'unsubscribed: %s' % self)
        self.room_ctrl.leave_room('delivery', self)
