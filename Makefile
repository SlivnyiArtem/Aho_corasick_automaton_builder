lint:
	isort .
	flake8 --config setup.cfg
	black --config pyproject.toml .