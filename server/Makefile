ifeq ($(VIRTUAL_ENV),)
	cmd = poetry run
else
	cmd = . $(VIRTUAL_ENV)/bin/activate && deactivate && poetry run
endif

run:
	docker-compose up --build

build:
	docker-compose build

test: build
	$(cmd) pytest -sv
