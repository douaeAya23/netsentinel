.PHONY: install lint format test

install:
	pip install -e ".[dev]"

lint:
	ruff check src tests

format:
	ruff format src tests

test:
	pytest