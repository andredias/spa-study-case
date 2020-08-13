run:
	python -m app.main


test:
	pytest -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/ --cov ../common/app/


docker-build:
	cd .. && docker build -t tornado_api -f Dockerfile.tornado_api .


docker-run: docker-build
	docker run -it --rm -p 8443:8443 --env-file .env -e ENV=development tornado_api
