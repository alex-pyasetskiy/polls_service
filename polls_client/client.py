import redis
import os
import json
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler, tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import urllib.request
import tornadoredis

from listener import RedisProvider

RC = redis.StrictRedis(db=2)

client = tornadoredis.Client(selected_db=2)
client.connect()


class PollsListHandler(RequestHandler):
    def get(self):
        with urllib.request.urlopen('http://localhost:8000/api/questions/') as response:
            data = response.read()
            result = data.decode(encoding='utf-8', errors='ignore')
            print(result)
            self.render('templates/index.html', polls_list=json.loads(result))


class RESTVoteHandler(RequestHandler):
    def post(self, *args, **kwargs):
        data = tornado.escape.json_decode(self.request.body)
        ureq = urllib.request.Request('http://localhost:8000/api/questions/%s/vote/?choice=%s' %
                                            (data['question_id'], data['choice_id']),
                                      method='PUT')
        urllib.request.urlopen(ureq)
        self.write("Complete")


class RedisMessageHandler(WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(RedisMessageHandler, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client(selected_db=2)
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'api_events')
        self.client.listen(self.on_message)

    def on_message(self, msg):
        if msg.kind == 'message':
            self.write_message(str(msg.body))
        if msg.kind == 'disconnect':
            # Do not try to reconnect, just send a message back
            # to the client and close the client connection
            self.write_message('The connection terminated '
                               'due to a Redis server error.')
            self.close()

    def on_close(self):
        pass


settings = {
    'auto_reload': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'debug':True
}

application = Application([
    (r'/', PollsListHandler),
    (r'/vote', RESTVoteHandler),
    (r'/ws/track_events', RedisMessageHandler)
], **settings)


if __name__ == "__main__":
    RedisProvider(RC, ['api_events']).start()
    http_server = HTTPServer(application)
    http_server.listen(8989)
    print('Demo is runing at localhost:8989\nQuit the demo with CONTROL-C')
    IOLoop.instance().start()