run:
	hypercorn --reload --config=hypercorn.toml 'app:create_app()'


test:
	pytest


docker_build:
	docker build -t fastapi_api .


docker_run: docker_build
	docker run -it --rm -p 8443:8443 --env-file .env fastapi_api
