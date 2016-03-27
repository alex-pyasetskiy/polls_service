import redis
import os
import json
from tornado.web import RequestHandler, Application
from tornado.websocket import WebSocketHandler
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import urllib.request
from tornado.autoreload import add_reload_hook


from listener import RedisProvider

RC = redis.StrictRedis(db=1)

class PollsListHandler(RequestHandler):
    def get(self):
        with urllib.request.urlopen('http://localhost:8000/api/questions/') as response:
            data = response.read()
            result = data.decode(encoding='utf-8',errors='ignore')
            print(result)
            self.render('templates/index.html', polls_list=json.loads(result))


class ClientVoteHandler(WebSocketHandler):
    def open(self):
        RedisProvider.add_listener(self)

    def on_message(self, message):
        print(message)
        req = json.loads(message)
        print(req)
        ureq = urllib.request.Request('http://localhost:8000/api/questions/%s/vote/?choice=%s' %
                                            (req['question_id'], req['choice_id']),
                                      method='PUT')
        with urllib.request.urlopen(ureq) as response:
            if response.status == 200:
                self.write_message(response.read())

    def on_close(self):
        pass


class RealtimeHandler(WebSocketHandler):
    def open(self):
        RedisProvider.add_listener(self)

    def on_message(self, message):
        print(message)

    def on_close(self):
        pass


settings = {
    'auto_reload': True,
    'static_path': os.path.join(os.path.dirname(__file__), "static"),
    'debug':True
}

application = Application([
    (r'/', PollsListHandler),
    (r'/ws/vote', ClientVoteHandler),
    (r'/realtime', RealtimeHandler),
], **settings)


if __name__ == "__main__":
    RedisProvider(RC, ['events', 'client_events']).start()
    http_server = HTTPServer(application)
    http_server.listen(8989)
    IOLoop.instance().start()