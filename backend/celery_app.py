import csv
import os
import time
from io import StringIO

from celery import Celery
from django.conf import settings
from django.db.models import Sum, F
from django.http import HttpResponse

from recipes.models import Ingredient

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram_backend.settings')

app = Celery('foodgram_backend')
app.config_from_object('django.conf:settings')
app.conf.broker_url = settings.CELERY_BROKER_URL
app.autodiscover_tasks()


@app.task()
def debug_task():
    time.sleep(20)
    print('Hello from debug_task :)')


@app.task()
def prepare_shopping_cart(request):
    header = ('Ингредиент', 'Единица измерения', 'Количество')
    query = (Ingredient.objects
             .filter(recipes__recipe__shopping__user=request.user)
             .annotate(amount=F('recipes__amount'))
             .annotate(sum_amount=Sum('amount'))
             .order_by('name'))
    with StringIO() as file:
        csv.writer(file).writerow(header)
        csv.writer(file).writerows(
            query.values_list('name', 'measurement_unit', 'sum_amount'))

        return HttpResponse(file.getvalue(), headers={
            'Content-Type': 'text/csv',
            'Content-Disposition':
                'attachment; filename="shopping_cart.csv"',
        })
        # return file.getvalue()
