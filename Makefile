# --------- CONFIG ---------
VENV_DIR := env
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip
LOG_LEVEL ?= INFO

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
	$(PYTHON) src/main.py --render-mode random --log-level $(LOG_LEVEL)

stream:
	$(PYTHON) src/main.py --mode stream --log-level $(LOG_LEVEL)

retrain:
	$(PYTHON) src/main.py --render-mode all --generate-sbert-data --log-level $(LOG_LEVEL)

test:
	$(PYTHON) -c "from sentence_transformers import SentenceTransformer; m = SentenceTransformer('all-MiniLM-L6-v2'); print(m.encode('hello')[:5])"

freeze:
	$(PIP) freeze > requirements.txt

clean:
	rm -rf __pycache__ env/ data/*.csv data/*.json

similarity:
	@read -p "Sentence 1: " s1; \
	read -p "Sentence 2: " s2; \
	PYTHONPATH=src $(PYTHON) -c "from utils.similarity import get_similarity_score; print(f'Score: {get_similarity_score(\"$$s1\", \"$$s2\")}')"

# ---------- Testing Utilities ----------
stream-debug:
	make stream LOG_LEVEL=debug

run-debug:
	make run LOG_LEVEL=debug

retrain-debug:
	make retrain LOG_LEVEL=debug

clean:
	rm -rf env data/*.csv data/*.json __pycache__ src/**/__pycache__ .pytest_cache
