from tornado import web as tornado_web
from tornado import ioloop as tornado_ioloop

from websocket_app.helpers import APIHelper
from websocket_app.rooms import RoomController

from handlers import CurrencyDeliveryHandler


def create_websocket_server(port, handlers, **settings_kwargs):
    app = tornado_web.Application(handlers, **settings_kwargs)
    app.listen(port)
    return tornado_ioloop.IOLoop.instance()


if __name__ == '__main__':
    settings = {
        'auto_reload': True,
    }
    server_port = 8081
    server = create_websocket_server(
        server_port,
        [(r'/currencies/',
          CurrencyDeliveryHandler,
          {
              'room_controller': RoomController('currencies_delivery'),
              'api_helper': APIHelper('http://localhost:8000/api/'),
              'app_name': 'currencies_delivery'
          })],
        **settings
    )
    print 'Tornado server is running on %d port ...' % server_port
    server.start()
