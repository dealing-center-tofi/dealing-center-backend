import logging

from websocket_app.handlers import WebSocketHandler


access_log = logging.getLogger("tornado.access")


class CurrencyDeliveryHandler(WebSocketHandler):
    def __init__(self, application, request, app_name, room_controller,
                 orders_room_controller, api_helper, **kwargs):
        super(CurrencyDeliveryHandler, self).__init__(application, request, app_name, **kwargs)
        self.room_ctrl = room_controller
        self.orders_room_ctrl = orders_room_controller
        self.api = api_helper
        self.user = None

    def on_close(self):
        super(CurrencyDeliveryHandler, self).on_close()
        self.room_ctrl.leave_rooms_for_client(self)
        self.orders_room_ctrl.leave_rooms_for_client(self)

    def register_events(self):
        self.events_handlers = {
            'authorize': self.authorize,
            'subscribe': self.subscribe,
            'unsubscribe': self.unsubscribe,
            'orders_closing_subscribe': self.orders_closing_subscribe,
            'orders_closing_unsubscribe': self.orders_closing_unsubscribe
        }

    def authorize(self, data):
        self.api.headers.update({'Authorization': 'Token %s' % data['token']})
        response = self.api.do_request('GET', '/users/me/')
        if response.status_code == 200:
            self.user = response.json()
            self.emit('authorized')
        else:
            pass

    def subscribe(self, data):
        if self.user is not None:
            access_log.log(logging.DEBUG, 'subscribed: %s' % self)
            self.room_ctrl.join_room('delivery', self)
        else:
            self.raise_client_error('User is not authorized')

    def unsubscribe(self, data):
        if self.user is not None:
            access_log.log(logging.DEBUG, 'unsubscribed: %s' % self)
            self.room_ctrl.leave_room('delivery', self)
        else:
            self.raise_client_error('User is not authorized')

    def orders_closing_subscribe(self, data):
        if self.user is not None:
            access_log.log(logging.DEBUG, 'orders_closing subscribed: %s' % self)
            self.orders_room_ctrl.join_room('orders_closing-user-%s' % self.user.get('id'), self)
        else:
            self.raise_client_error('User is not authorized')

    def orders_closing_unsubscribe(self, data):
        if self.user is not None:
            access_log.log(logging.DEBUG, 'orders_closing unsubscribed: %s' % self)
            self.orders_room_ctrl.leave_room('orders_closing-user-%s' % self.user.get('id'), self)
        else:
            self.raise_client_error('User is not authorized')
