check:
	@echo
	isort --diff -c --skip-glob '**.venv' .
	@echo
	yapf -vv --diff --recursive --style yapf.ini --exclude '**.venv' .
	@echo
	mypy fastapi_api
	mypy quart_api
	@echo
	flake8 --config flake8.ini .
