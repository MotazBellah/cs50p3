web: gunicorn restaurant.wsgi --log-file -
worker: celery -A restaurant worker -l info
