POSTGRESQL_RUNNING = $(shell docker ps | grep postgres-development)
REDIS_RUNNING = $(shell docker ps | grep redis-development)

run:
	hypercorn --reload --config=hypercorn.toml 'app:create_app()'


test:
	ENV=testing pytest -x -v --cov-report term-missing --cov-report html --cov-branch --cov app/ --cov ../common/app/


docker-build:
	cd .. && docker build -t fastapi_api -f Dockerfile.fastapi_api .


docker-run: docker-build
	docker run -it --rm -p 8443:8443 -e ENV=development fastapi_api


start-containers:
	docker-compose up -d


stop-postgres:
	@ if [ -n "$(POSTGRESQL_RUNNING)" ]; then \
	echo 'Stopping PostgreSQL...'; \
	docker stop postgres-development; \
	fi
