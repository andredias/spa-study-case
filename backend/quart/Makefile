.PHONY: install run test env

env:
	echo "QUART_ENV=development\n\
	QUART_APP=\n\
	" > .env


install: env
	pip install poetry
	poetry install
	poetry run flaquartsk deploy


run:
	ENV=development QUART_APP='app:create_app()' poetry run quart run


test:
	poetry run pytest
