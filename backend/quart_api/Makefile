run:
	hypercorn --reload --config=hypercorn.toml "app:create_app()"
	# curl --insecure -v https://127.0.0.1:8443/hello
	# http --verify no https://localhost:8443/hello


test:
	pytest


docker_build:
	docker build -t quart_api .


docker_run: docker_build
	docker run -it --rm -p 8443:8443 -p 4433:4433 -e ENV=production quart_api
