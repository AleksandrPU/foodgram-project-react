# Generated by Django 3.2.3 on 2024-01-13 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_recipeingredient_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'verbose_name': 'ингредиент для рецепта', 'verbose_name_plural': 'Ингредиенты для рецепта'},
        ),
    ]