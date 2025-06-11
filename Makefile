.PHONY:help lint test web clean

help:
	@echo "Available commands are: \n*lint test web and clean"

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

clean:
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf risk_of_bias/__pycache__/
	rm -rf risk_of_bias/*/__pycache__/
	rm -rf risk_of_bias/*/*/__pycache__/
	rm -rf tests/__pycache__/
	rm -rf *.egg-info/
	rm -rf build/
	rm -rf dist/
	rm -rf site/
	rm -rf .venv/
	rm -rf venv/
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
