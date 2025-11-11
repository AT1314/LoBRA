VENV=.venv
PY=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv deps ingest ingest-incremental ask clean verify setup test pipeline install-pipeline watch

venv:
	python3 -m venv $(VENV)

deps: venv
	$(PIP) install -U pip
	$(PIP) install -r requirements.txt
	# NLTK tokenizer (once)
	@$(PY) -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('punkt_tab', quiet=True); nltk.download('stopwords', quiet=True)"

ingest:
	$(PY) scripts/ingest-smart.py

ingest-full:
	$(PY) scripts/ingest.py

ask:
	@q='$(q)'; if [ -z "$$q" ]; then echo 'Usage: make ask q="your question"'; exit 1; fi
	$(PY) scripts/query.py --q "$$q"

clean:
	rm -rf brain/* logs/*

verify:
	@./verify.sh

setup:
	@./setup.sh

test:
	@./test-system.sh

install-pipeline: venv
	$(PIP) install -r requirements-pipeline.txt

install-ui: venv
	$(PIP) install -r requirements-ui.txt

ui:
	$(PY) -m streamlit run app.py --server.port 8501

pipeline:
	$(PY) scripts/preprocess.py

ingest-incremental:
	$(PY) scripts/ingest-incremental.py

watch:
	@echo "Watching inbox/ for new files (Ctrl+C to stop)..."
	@while true; do \
		if [ -n "$$(ls -A inbox 2>/dev/null | grep -v '^\.')" ]; then \
			$(PY) scripts/preprocess.py; \
		fi; \
		sleep 5; \
	done

