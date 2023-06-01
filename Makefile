.PHONY: local

local:
	python manage.py runserver
check:
	python manage.py check
migration:
	python manage.py runserver makemigrations
migrate:
	python manage.py runserver migrate
# handmatig pre-commit
lint:
	pre-commit run -a
# pip-tools commands
dev-compile:
	pip-compile reqs/dev.in
req-compile:
	pip-compile reqs/req.in
# django_extention commands
rs-ex:
	python manage.py runserver_plus --nopin
shell:
	python manage.py shell_plus --ipython #use tab to see autocompl
models:
	python manage.py list_model_info
help-admin:
	python manage.py admin_generator my_app
url:
	python manage.py show_urls
