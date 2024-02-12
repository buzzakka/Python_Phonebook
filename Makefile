PYTHON = python3
REQUIREMENTS = rerequirements.txt

all: test

#	== Тестирование ==
.PHONY: test
test:
	@echo -------------------- RUN TESTS --------------------
	$(PYTHON) -m unittest discover .

#	== Отчистка от временных файлов ==
.PHONY: clean
clean:
	@echo -------------------- CLEAN --------------------
	rm -rf src/__pycache__ tests/__pycache__

#	== Установка виртуального окружения ==
.PHONY: venv
venv:
    @echo -------------------- INSTALL VENV --------------------
	python -m venv venv
	source venv/bin/activate
	pip install -r $(REQUIREMENTS)
