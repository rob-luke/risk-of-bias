.PHONY:help lint test 

help:
	@echo "Available commands are: \n*lint and test"

lint:
	black .
	isort .
	mypy .
	codespell .

lint-check:
	black --check .
	isort --check .
	mypy --check .
	codespell .

test:
	pytest .