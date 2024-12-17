all: django

config:
	python -m immunity_agent -h

django:
	python manage.py runserver

flask:
	python test_flask.py

.PHONY: django flask