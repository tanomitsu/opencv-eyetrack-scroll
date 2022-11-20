init:
	poetry install

test:
	pytest tests

run:
	python -m src

.PHONY: init test