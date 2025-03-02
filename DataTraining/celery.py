import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DataTraining.settings')

app = Celery('DataTraining', broker='redis://127.0.0.1:6379', backend = 'redis://127.0.0.1:6379')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

CELERYD_USER="celery"
CELERYD_GROUP="celery"

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')