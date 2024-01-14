import csv

from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


def import_ingredients(file):
    try:
        with open(file) as csvfile:
            reader = csv.reader(csvfile)
            for name, unit in reader:
                Ingredient.objects.get_or_create(
                    name=name, measurement_unit=unit)
    except FileNotFoundError:
        raise CommandError(f'Файл {file} не найден!')
    except Exception as error:
        raise CommandError(error)


class Command(BaseCommand):
    help = 'Импорт ингредиентов из CSV.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv',
            help='Укажите CSV для загрузки.'
        )

    def handle(self, *args, **options):
        if file := options['csv']:
            import_ingredients(file)
            self.stdout.write(self.style.SUCCESS('Данные загружены'))
        else:
            self.stderr.write(self.style.ERROR('Не указан CSV для загрузки!'))
