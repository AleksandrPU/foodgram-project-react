from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from recipes.filters import RecipeFilterSet
from recipes.serializers import (
    IngredientSerializer,
    RecipeReadSerializer,
    RecipeCreateSerializer,
    TagSerializer
)

from recipes.models import Ingredient, Recipe, Tag


User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilterSet
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)
