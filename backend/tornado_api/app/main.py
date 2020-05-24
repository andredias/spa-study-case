import sys
from pathlib import Path
from typing import Union

from dotenv import load_dotenv
from loguru import logger
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from .api import HelloHandler


def create_app(env_filename: Union[str, Path] = '.env') -> Application:

    # a .env file is not mandatory.
    # You can specify envvar parameters by other means
    # as long as they are available before config is imported
    load_dotenv(env_filename)

    from . import config

    # config logger
    logger.remove()  # remove standard handler
    logger.add(
        sys.stderr, level=config.LOG_LEVEL, colorize=True, backtrace=config.DEBUG, enqueue=True
    )  # reinsert it to make it run in a different thread
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
