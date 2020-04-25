.PHONY: install run test env

env:
	echo "QUART_ENV=development\n\
	QUART_APP=\n\
	" > .env

run:
	ENV=development QUART_APP='app:create_app()' quart run


test:
	pytest
