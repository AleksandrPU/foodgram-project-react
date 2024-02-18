import csv
from io import StringIO

from celery import shared_task
from django.db.models import F, Sum
from django.http import HttpResponse

from recipes.models import Ingredient


@shared_task
def prepare_shopping_cart(user_id):
    header = ('Ингредиент', 'Единица измерения', 'Количество')
    query = (Ingredient.objects
             .filter(recipes__recipe__shopping__user__pk=user_id)
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
