run:
	QUART_APP="app:create_app()" quart run


test:
	pytest


live_server:
	hypercorn --certfile tests/certificates/server.pem --keyfile tests/certificates/server.key \
	          --config=tests/hypercorn.toml "app:create_app()"
	# curl --cacert tests/certificates/client.pem https://127.0.0.1:8443/hello
	# http --verify no http://localhost:8443/hello
