.PHONY: install lint format test prepare eda

install:
	pip install -e ".[dev]"

lint:
	ruff check src tests

format:
	ruff format src tests

test:
	pytest

prepare:
	python -m netsentinel.jobs.prepare_data

eda:
	python -m netsentinel.jobs.run_eda