release: python manage.py migrate
web: gunicorn cardealer.wsgi:application --bind 127.0.0.1:8000 --timeout 120
