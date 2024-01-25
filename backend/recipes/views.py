import csv
from io import StringIO
from pprint import pprint

from django.contrib.auth import get_user_model
from django.db.models import F, Sum
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
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

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def add_delete_favorite_shopping_cart(self, request, model, pk=None):
        ERROR_MESSAGE_ADD = (
            f'Ошибка добавления в {Favorite._meta.verbose_name}:')
        ERROR_MESSAGE_DELETE = (
            f'Ошибка удаления из {Favorite._meta.verbose_name}:')

        recipe = self.get_object()
        user = request.user

        if request.method == 'POST':
            if model.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'errors': f'{ERROR_MESSAGE_ADD} '
                               'Рецепт уже есть в '
                               f'{Favorite._meta.verbose_name}.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                model.objects.create(user=user, recipe=recipe)
            except Exception as error:
                return Response(
                    {'errors': f'{ERROR_MESSAGE_ADD} {error}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response({
                'id': recipe.id,
                'name': recipe.name,
                'image': self.get_image_url(recipe),
                'cooking_time': recipe.cooking_time,
            },
                status=status.HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if obj := model.objects.filter(user=user, recipe=recipe):
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
                {'errors': f'{ERROR_MESSAGE_DELETE} Рецепта нет в '
                           f'{Favorite._meta.verbose_name}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk=None):
        return self.add_delete_favorite_shopping_cart(
            request, Favorite, pk=None)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk=None):
        return self.add_delete_favorite_shopping_cart(
            request, ShoppingCart, pk=None)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        header = ('Ингредиент', 'Единица измерения', 'Количество')
        query = (Ingredient.objects
                 .filter(recipes__recipe__shopping__user=request.user)
                 .annotate(amount=F('recipes__amount'))
                 .annotate(amount=Sum('amount'))
                 .order_by('name'))
        with StringIO() as file:
            csv.writer(file).writerow(header)
            csv.writer(file).writerows(
                query.values_list('name', 'measurement_unit', 'amount'))

            return HttpResponse(file.getvalue(), headers={
                'Content-Type': 'text/csv',
                'Content-Disposition':
                    'attachment; filename="shopping_cart.csv"',
            })


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilterSet
