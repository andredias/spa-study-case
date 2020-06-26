import ujson as json
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    @property
    def args(self):
        return json.loads(self.request.body)
