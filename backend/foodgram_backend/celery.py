import os
import time

from celery import Celery
# from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'foodgram_backend.settings')

# app = Celery('foodgram_backend', broker='redis://redis:6379/0')
app = Celery('foodgram_backend')

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    time.sleep(20)
    print(f'Request: {self.request!r}')
