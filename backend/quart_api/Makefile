run:
	hypercorn --reload --config=hypercorn.toml 'app:create_app()'


test:
	pytest -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/


docker-build:
	cd .. && docker build -t quart_api -f Dockerfile.quart_api .


docker-run: docker-build
	docker run -it --rm -p 8443:8443 --env-file .env quart_api
