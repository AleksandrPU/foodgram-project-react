from pprint import pprint

from django.contrib import admin
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class IngredientsInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    inlines = (IngredientsInline,)


admin.site.register(Tag)
