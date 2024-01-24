# todo
from pprint import pprint

from django.db.models import Case, Q, Value, When
from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


# todo
class RecipeFilterSet(filters.FilterSet):
    author = filters.NumberFilter(field_name='author')
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='favorited_filter')
    # 'is_in_shopping_cart',

    class Meta:
        model = Recipe
        # fields = ('author', 'tags', 'is_favorited')
        fields = ('author', 'tags')

    def favorited_filter(self, queryset, name, value):
        print('******************')
        pprint(self.__dict__)
        print(queryset)
        print(name)
        print(value)
        print('******************')
        user = self.request.user
        print(user)
        if user.is_authenticated:
            return user.favorites.all()
        return queryset


# todo
class IngredientFilterSet(filters.FilterSet):
    name = filters.CharFilter(method='name_filter')

    class Meta:
        model = Ingredient
        fields = ('name',)

    def name_filter(self, queryset, name, value):
        query_istartswith = Q(name__istartswith=value)
        query_icontains = Q(name__icontains=value)
        return (queryset.filter(query_istartswith | query_icontains)
                .annotate(search_type_ordering=Case(
                    When(query_istartswith, then=Value(1)),
                    When(query_icontains, then=Value(0)),
                )).order_by('-search_type_ordering',))
