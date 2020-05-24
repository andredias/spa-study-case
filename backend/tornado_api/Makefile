run:
	python -m app.main


test:
	pytest -x -v --cov-report term-missing --cov app/


docker_build:
	docker build -t tornado_api .


docker_run: docker_build
	docker run -it --rm -p 8443:8443 --env-file .env tornado_api
