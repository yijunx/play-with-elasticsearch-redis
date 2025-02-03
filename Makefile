test:
	@clear
	@pytest -s --durations=0 -v --cov=app

format:
	@isort app/
	@isort tests/
	@black app/
	@black tests/