# Generated by Django 3.2.3 on 2024-02-23 06:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_ingredientrecipe_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#0000ff', max_length=7, verbose_name='Цвет'),
        ),
    ]