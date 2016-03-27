import threading


class RedisProvider(threading.Thread):
    _LISTENERS = []

    def __init__(self, redis_client, channels):
        threading.Thread.__init__(self)
        self.redis = redis_client
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)

    def run(self):
        for item in self.pubsub.listen():
            for element in self._LISTENERS:
                element.write_message(item['data'])

    @classmethod
    def add_listener(cls, listener):
        cls._LISTENERS.append(listener)