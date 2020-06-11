from tornado.web import RequestHandler


class HelloHandler(RequestHandler):

    def get(self):
        self.write({'hello': 'world'})
