from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.filters import IngredientFilterSet, RecipeFilterSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.paginations import CustomPageNumberPagination
from recipes.permissions import IsAuthorOrReadOnly
from recipes.serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    TagSerializer
)


User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    # todo
    # pagination_class = LimitOffsetPagination
    filterset_class = RecipeFilterSet
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    # todo maybe decorator
    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk=None):
        ERROR_MESSAGE_ADD = 'Ошибка добавления в избранное:'
        ERROR_MESSAGE_DELETE = 'Ошибка удаления из избранного:'

        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.get(user=user, recipe=recipe):
                return Response(
                    {'errors': f'{ERROR_MESSAGE_ADD} '
                               'Рецепт уже есть в избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                Favorite.objects.create(user=user, recipe=recipe)
            except Exception as error:
                return Response(
                    {'errors': f'{ERROR_MESSAGE_ADD} {error}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response({
                'id': recipe.id,
                'name': recipe.name,
                'image': recipe.image,
                'cooking_time': recipe.cooking_time,
            },
                status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if obj := Favorite.objects.get(user=user, recipe=recipe):
                try:
                    obj.delete()
                except Exception as error:
                    return Response(
                        {'errors': f'{ERROR_MESSAGE_DELETE} {error}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': f'{ERROR_MESSAGE_DELETE} Рецепта нет в избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # todo maybe decorator
    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        ERROR_MESSAGE_ADD = 'Ошибка добавления в список покупок:'
        ERROR_MESSAGE_DELETE = 'Ошибка удаления из списка покупок:'

        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if ShoppingCart.objects.get(user=user, recipe=recipe):
                return Response(
                    {'errors': f'{ERROR_MESSAGE_ADD} '
                               'Рецепт уже есть в списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                ShoppingCart.objects.create(user=user, recipe=recipe)
            except Exception as error:
                return Response(
                    {'errors': f'{ERROR_MESSAGE_ADD} {error}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response({
                'id': recipe.id,
                'name': recipe.name,
                'image': recipe.image,
                'cooking_time': recipe.cooking_time,
            },
                status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if obj := ShoppingCart.objects.get(user=user, recipe=recipe):
                try:
                    obj.delete()
                except Exception as error:
                    return Response(
                        {'errors': f'{ERROR_MESSAGE_DELETE} {error}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': f'{ERROR_MESSAGE_DELETE} Рецепта нет в избранном.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    # todo
    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        pass


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilterSet
