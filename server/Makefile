ifeq ($(VIRTUAL_ENV),)
	cmd = poetry run
else
	cmd = . $(VIRTUAL_ENV)/bin/activate && deactivate && poetry run
endif

RANDOM_PASSWORD=$(shell date | md5sum | cut -f 1 -d ' ')

run: env_file
	docker-compose up --build

.env:
	sed "s/DB_PASSWORD=.*/DB_PASSWORD=$(RANDOM_PASSWORD)/" env.template > .env

env_file: .env

build:
	docker-compose build

test: env_file build
	$(cmd) pytest -sv
