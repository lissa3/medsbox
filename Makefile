rs:
	python manage.py runserver
rs-ex:
	python manage.py runserver_plus --nopin
check:
	python manage.py check
migration:
	python manage.py runserver makemigrations
migrate:
	python manage.py runserver migrate
lint:
	pre-commit run -a
shell:
	python manage.py shell_plus --ipython #use tab to see autocompl
models:
	python manage.py list_model_info
help-admin:
	python manage.py admin_generator my_app
url:
	python manage.py show_urls





