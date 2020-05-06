run:
	QUART_APP="app:create_app()" quart run --port 8080


test:
	pytest


live_server:
	hypercorn --certfile=cert/server.pem --keyfile=cert/server.key --config=hypercorn.toml "app:create_app()"
	# curl --cacert certificates/client.pem https://127.0.0.1:8443/hello
	# http --verify no http://localhost:8443/hello


docker_build:
	docker build -t quart_api .


docker_run: docker_build
	docker run -it --rm -p 8443:8443 -p 4433:4433 \
	           -e ENV=production -e CERTFILE=cert/server.pem -e KEYFILE=cert/server.key \
	           -v `pwd`/cert:/app/cert quart_api