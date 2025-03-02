web: gunicorn DataTraining.wsgi --log-file -
worker: cd /app && pip install pkgutil-resolve-name && celery -A DataTraining worker --loglevel=info