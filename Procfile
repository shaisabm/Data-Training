web: gunicorn DataTraining.wsgi --log-file -
worker: celery -A DataTraining worker --loglevel=info