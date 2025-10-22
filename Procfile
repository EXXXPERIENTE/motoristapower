web: python manage.py migrate && gunicorn fleet.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate
