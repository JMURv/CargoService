start:
	poetry run python manage.py runserver

shell:
	poetry run python manage.py shell

load-data:
	poetry run python manage.py load_initial_data .\api\management\files\uszips.csv

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

celery:
	celery --app=CargoService worker --loglevel=info --pool=solo

beat:
	celery -A CargoService beat -l info

flash-start:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate
	poetry run python manage.py load_initial_data .\api\management\files\uszips.csv
	poetry run python manage.py runserver