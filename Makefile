REQUIREMENTS = requirements.txt
BIN = ./venv/bin/
BIN_PYTHON3 = $(BIN)python3
PYTHON = python3

all: venv run_app

#	== Тестирование ==
.PHONY: test
test:
	@echo -------------------- RUN TESTS --------------------
	$(BIN_PYTHON3) -m unittest discover .

#	== Отчистка от временных файлов ==
.PHONY: clean
clean:
	@echo -------------------- CLEAN --------------------
	rm -rf src/__pycache__ tests/__pycache__

#	== Установка виртуального окружения ==
.PHONY: venv
venv:
	@echo -------------------- INSTALL VENV --------------------
	$(PYTHON) -m venv venv
	$(BIN)pip3 install -r $(REQUIREMENTS)

.PHONY: run_app
run_app:
	$(BIN_PYTHON3) app.py