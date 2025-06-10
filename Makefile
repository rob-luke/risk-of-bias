.PHONY:help lint test 

help:
	@echo "Available commands are: \n*lint and test"

lint:
	black .
	isort .
	mypy .
	flake8 --max-line-length=88 risk_of_bias
	codespell .

lint-check:
	black --check .
	isort --check .
	mypy --check .
	flake8 --max-line-length=88 risk_of_bias
	codespell .

test:
	pytest .