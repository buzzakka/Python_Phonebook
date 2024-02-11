PYTHON = python3

all: test

test:
	$(PYTHON) -m unittest discover .
