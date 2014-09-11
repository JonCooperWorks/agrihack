test:
	@./backend/run_unit_tests.py


serve:
	dev_appserver.py \
	--host=localhost \
	--port=8080 \
	.

pyflakes:
	@pyflakes .


pep8:
	@pep8 --exclude="venv" .


bootstrap:
	@pip install -r testing_requirements.txt --use-mirrors
