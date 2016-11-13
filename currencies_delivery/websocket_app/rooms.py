import brukva

from mixins import RedisAppNameMixin


class Room(RedisAppNameMixin):
    def __init__(self, name, app_name):
        self.redis_app_name = app_name
        self.name = name
        self.clients = set()
        self._init_redis_listener()

    def _init_redis_listener(self):
        self.redis_client = brukva.Client()
        self.redis_client.connect()
        self.redis_client.subscribe('%s#%s#' % (self.get_redis_app_name(), self.name))
        self.redis_client.listen(self.on_messages_published)

    def on_messages_published(self, message):
        for client in self.clients:
            client.write_message(message.body)

    def unsubscribe(self):
        self.redis_client.unsubscribe('%s#%s#' % (self.get_redis_app_name(), self.name))


class RoomController(object):
    def __init__(self, app_name):
        self.app_name = app_name
        self.rooms = set()

    def join_room(self, room_name, client):
        self.get_or_create_room(room_name).clients.add(client)

    def leave_room(self, room_name, client):
        room = self.get_or_create_room(room_name)
        room.clients.discard(client)
        if not room.clients:
            self.rooms.remove(room)
            room.unsubscribe()

    def leave_rooms_for_client(self, client):
        matter_rooms = filter(lambda room: client in room.clients, self.rooms)
        for room in matter_rooms:
            self.leave_room(room.name, client)

    def get_or_create_room(self, room_name):
        matter_rooms = filter(lambda x: x.name == room_name, self.rooms)
        if matter_rooms:
            room = matter_rooms.pop(0)
        else:
            room = Room(room_name, self.app_name)
            self.rooms.add(room)
        return room
