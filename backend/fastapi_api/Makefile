run:
	hypercorn --reload --config=hypercorn.toml 'app:create_app()'


test:
	ENV=testing pytest -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/ --cov ../common/app/


test_prod:
	ENV=production pytest -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/ --cov ../common/app/


docker_build:
	docker build -t fastapi_api .


docker_run: docker_build
	docker run -it --rm -p 8443:8443 -e ENV=development fastapi_api
