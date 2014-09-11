test:
	@./backend/run_unit_tests.py


serve:
	@$(PYTHON) $(APPENGINE)/dev_appserver.py \
		--host=$(SERVE_ADDRESS) \
		--port=$(SERVE_PORT) \
		.

pyflakes:
	@pyflakes .


pep8:
	@pep8 --exclude="venv" .
