Created with::

    openssl req -x509 -newkey rsa:2048 -keyout server.key -out server.pem -days 36500 --nodes -subj '/CN=localhost'
