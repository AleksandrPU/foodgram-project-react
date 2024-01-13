import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


def import_ingredients():
    try:
        with open('../../data/ingredients.csv') as csvfile:
            reader = csv.reader(csvfile)
            for name, unit in reader:
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit)
    except FileNotFoundError:
        raise ValueError('ingredients.csv не найден!')
    except Exception as error:
        print(error)


class Command(BaseCommand):
    help = 'Импорт ингредиентов из CSV'

    def handle(self, *args, **options):
        import_ingredients()
        self.stderr.write(self.style.SUCCESS('Данные загружены'))
