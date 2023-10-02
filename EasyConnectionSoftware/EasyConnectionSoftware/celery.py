import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EasyConnectionSoftware.settings')
app = Celery('scheduler')
app.config_from_object('django.conf:settings',namespace='CELERY')

@app.task
def add_numbers():
    return


app.autodiscover_tasks()