from django.db.models import Q
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    STATUS_CHOICES = (
        (0, False),
        (1, True)
    )
    author = filters.NumberFilter(field_name='author')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.ChoiceFilter(
        method='favorited_filter', choices=STATUS_CHOICES)
    is_in_shopping_cart = filters.ChoiceFilter(
        method='shopping_filter', choices=STATUS_CHOICES)

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def favorited_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(favorites__user=user)
            else:
                return queryset.filter(~Q(favorites__user=user))
        return queryset

    def shopping_filter(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated:
            if value == '1':
                return queryset.filter(shopping__user=user)
            else:
                return queryset.filter(~Q(shopping__user=user))
        return queryset


class IngredientFilterSet(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='startswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
