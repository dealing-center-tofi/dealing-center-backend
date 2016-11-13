class RedisAppNameMixin(object):
    redis_app_name = None

    def get_redis_app_name(self):
        assert self.redis_app_name is not None, 'redis_app_name must be specified'
        return 'tornado-%s' % self.redis_app_name
