all: django

config:
	python3 -m immunity_agent -h

django:
	python3 manage.py runserver

flask:
	python3 test_flask.py

.PHONY: django flask