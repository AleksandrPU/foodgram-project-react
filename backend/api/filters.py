from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag


class RecipeFilterSet(filters.FilterSet):
    author = filters.NumberFilter(field_name='author')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags',)
