# Generated by Django 3.2.3 on 2024-02-22 19:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.RegexValidator('^[0-9]+$', 'Значение должно быть целым числом')]),
        ),
    ]
