import os
import time

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'foodgram_backend.settings')

app = Celery('foodgram_backend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    time.sleep(20)
    print(f'Request: {self.request!r}')
