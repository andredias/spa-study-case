import sys

from loguru import logger
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from . import config
from .api import HelloHandler


def create_app():
    # config logger
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=config.LOG_LEVEL, colorize=True, backtrace=config.LOG_BACKTRACE, enqueue=True
    )  # reinsert it to make it run in a different thread
    logger.add(config.LOG_FILENAME, level=config.LOG_LEVEL, backtrace=config.LOG_BACKTRACE, enqueue=True)
    logger.debug({key: getattr(config, key) for key in dir(config) if key == key.upper()})

    # Application setup
    app = Application(
        [
            (r"/hello", HelloHandler),
        ],
        debug=config.DEBUG,
    )
    return app


if __name__ == '__main__':
    import ssl

    app = create_app()

    port = 8443
    ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_ctx.load_cert_chain('cert/server.pem', 'cert/server.key')
    http_server = HTTPServer(app, ssl_options=ssl_ctx)
    http_server.listen(port)
    logger.info(f'Listening to port {port} over https (use CTRL + C to quit)')
    IOLoop.current().start()
