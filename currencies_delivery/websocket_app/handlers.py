import json

from redis import Redis
import tornado.websocket

from mixins import RedisAppNameMixin

redis = Redis()


class WebSocketHandler(RedisAppNameMixin, tornado.websocket.WebSocketHandler):
    def __init__(self, application, request, app_name, **kwargs):
        super(WebSocketHandler, self).__init__(application, request, **kwargs)
        self.redis_app_name = app_name
        self.events_handlers = None
        self.register_events()

    def open(self, *args):
        print('Open', self)

    def on_message(self, message):
        data = json.loads(message)
        event, data = data[:]
        event_handler = self.get_event_handler(event)
        if event_handler is not None:
            event_handler(data)
        else:
            self.emit('client error')

    def on_close(self):
        print 'Disconnected', self

    def check_origin(self, origin):
        return True

    def emit(self, event, *data_args):
        self.write_message(self.dump_data(event, *data_args))

    def broadcast_to(self, room, event, data):
        redis.publish('%s#%s#' % (self.get_redis_app_name(), room), self.dump_data(event, data))

    def dump_data(self, *args):
        return json.dumps(args)

    def get_event_handler(self, event):
        return self.events_handlers.get(event)

    def register_events(self):
        self.events_handlers = {}
