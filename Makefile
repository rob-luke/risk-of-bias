.PHONY:help lint test web

help:
	@echo "Available commands are: \n*lint test and web"

lint:
	black .
	isort .
	mypy .
	flake8 --max-line-length=88 --exclude risk_of_bias/web.py risk_of_bias
	codespell .

lint-check:
	black --check .
	isort --check .
	mypy --check .
	flake8 --max-line-length=88 --exclude risk_of_bias/web.py risk_of_bias
	codespell .

test:
	pytest .

web:
	uvicorn risk_of_bias.web:app --reload
