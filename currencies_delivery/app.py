import logging

from tornado import web as tornado_web
from tornado import ioloop as tornado_ioloop
from tornado import options as tornado_options

from websocket_app.helpers import APIHelper
from websocket_app.rooms import RoomController

from handlers import CurrencyDeliveryHandler


access_log = logging.getLogger("tornado.access")


def create_websocket_server(port, handlers, **settings_kwargs):
    app = tornado_web.Application(handlers, **settings_kwargs)
    app.listen(port)
    return tornado_ioloop.IOLoop.instance()


if __name__ == '__main__':
    tornado_options.parse_command_line()

    settings = {
        'auto_reload': True,
    }
    server_port = 8080
    server = create_websocket_server(
        server_port,
        [(r'/websocket/currencies/',
          CurrencyDeliveryHandler,
          {
              'room_controller': RoomController('currencies_delivery'),
              'orders_room_controller': RoomController('orders_closing_delivery'),
              'api_helper': APIHelper('http://localhost:8000/api'),
              'app_name': 'currencies_delivery'
          })],
        **settings
    )
    access_log.log(logging.INFO, 'Tornado server is running on %d port ...' % server_port)
    server.start()
