# --------- CONFIG ---------
VENV_DIR := env
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# --------- COMMANDS ---------
.PHONY: help setup run stream test clean freeze retrain

help:
	@echo ""
	@echo "Makefile for OSAI Demo 🚀"
	@echo "Usage:"
	@echo "  make setup        Create virtualenv & install requirements"
	@echo "  make run          Run the pipeline with default file input"
	@echo "  make stream       Start streaming input from stdin"
	@echo "  make test         Run SBERT test"
	@echo "  make freeze       Regenerate requirements.txt"
	@echo "  make retrain      Generate SBERT training pairs"
	@echo "  make clean        Delete env and temp data files"
	@echo ""

setup:
	python3 -m venv $(VENV_DIR)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) src/main.py --render-mode random

stream:
	$(PYTHON) src/main.py --mode stream

retrain:
	$(PYTHON) src/main.py --render-mode all --generate-sbert-data

test:
	$(PYTHON) -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello')[:5])"

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf __pycache__ env/ data/*.csv data/*.json
