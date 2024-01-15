from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.filters import RecipeFilterSet
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)
from recipes.models import Ingredient, Recipe, Tag


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilterSet


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
