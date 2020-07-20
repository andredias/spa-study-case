ifeq ($(VIRTUAL_ENV),)
	cmd = poetry run
else
	cmd = . $(VIRTUAL_ENV)/bin/activate && deactivate && poetry run
endif

RANDOM_PASSWORD=$(shell date | md5sum | cut -f 1 -d ' ')

run:
	if [ ! -f '.env' ]; then sed "s/DB_PASSWORD=.*/DB_PASSWORD=$(RANDOM_PASSWORD)/" env.template > .env; fi
	docker-compose up --build

build:
	docker-compose build

test: build
	$(cmd) pytest -sv
