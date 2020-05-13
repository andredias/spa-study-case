ifeq ($(VIRTUAL_ENV),)
	cmd = poetry run
else
	cmd = . $(VIRTUAL_ENV)/bin/activate && deactivate && poetry run
endif

build_images:
	docker-compose build

live_server: build_images
	docker-compose up

test:
	$(cmd) pytest
