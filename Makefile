
python := poetry run python3
black := poetry run black

install:
	poetry install

run:
	${python} pipeline.py

format:
	${black} sumreader
	${black} pipeline.py