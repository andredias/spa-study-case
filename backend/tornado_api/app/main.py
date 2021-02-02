from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Union

from dotenv import load_dotenv
from loguru import logger
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from . import config
from .handlers import hello, login, user
from .resources import shutdown, startup

routes = [
    ("/hello", hello.HelloHandler),
    ("/login", login.LoginHandler),
    ("/logout", login.LogoutHandler),
    ("/user", user.UserHandler),
    (r"/user/(\d+)", user.UserHandler),
]


@contextmanager
def create_app(env_filename: Union[str, Path] = None) -> Iterator[Application]:
    if env_filename:
        load_dotenv(env_filename)
    config.init()
    IOLoop.current().run_sync(startup)
    try:
        # Application setup
        settings = {
            "cookie_secret": config.SECRET_KEY,
            # "xsrf_cookies": True,
            "autoreload": True,
            "debug": config.DEBUG,
        }
        app = Application(routes, **settings)
        yield app
    finally:
        IOLoop.current().run_sync(shutdown)


if __name__ == '__main__':
    import ssl

    with create_app() as app:
        port = 8443
        ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_ctx.load_cert_chain('cert/server.pem', 'cert/server.key')
        http_server = HTTPServer(app, ssl_options=ssl_ctx)
        http_server.listen(port)
        logger.info(f'Listening to port {port} over https (use CTRL + C to quit)')
        IOLoop.current().start()
