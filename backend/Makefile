check:
	@echo
	yapf --diff --recursive --style yapf.ini --exclude '**.venv' .
	@echo
	mypy quart_api
	@echo
	flake8 --config flake8.ini .
