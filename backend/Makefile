check:
	@echo
	yapf --diff --recursive --style yapf.ini --exclude .venv --exclude '*/.venv' .
	@echo
	mypy quart
	@echo
	flake8 --config flake8.ini .