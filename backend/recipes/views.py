import csv
from io import StringIO

from django.contrib.auth import get_user_model
from django.db.models import Exists, F, OuterRef, Sum
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram_backend.paginations import CustomPageNumberPagination
from recipes.filters import IngredientFilterSet, RecipeFilterSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from recipes.permissions import IsAuthorOrReadOnly
from recipes.serializers import (
    FavoriteSerializer,
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeReadSerializer,
    RecipeShortSerializer,
    ShoppingCartSerializer,
    TagSerializer
)

User = get_user_model()


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    filterset_class = RecipeFilterSet
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Recipe.objects.all()
        return (Recipe.objects
                .annotate(is_favorited=Exists(
                    Favorite.objects
                    .filter(recipe=OuterRef('pk'), user=user)))
                .annotate(is_in_shopping_cart=Exists(
                    ShoppingCart.objects
                    .filter(recipe=OuterRef('pk'), user=user)))
                )

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeReadSerializer

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def add_delete_favorite_shopping_cart(self, request, model, pk=None):
        user = request.user

        if request.method == 'DELETE':
            recipe = self.get_object()
            if obj := model.objects.filter(user=user, recipe=recipe):
                obj.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'errors': 'Рецепта нет в '
                           f'{model._meta.verbose_name}.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if model is Favorite:
            model_serializer = FavoriteSerializer
        else:
            model_serializer = ShoppingCartSerializer

        serializer = model_serializer(
            data={'user': user.id, 'recipe': pk})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(
            RecipeShortSerializer(
                instance.recipe,
                context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def favorite(self, request, pk=None):
        return self.add_delete_favorite_shopping_cart(
            request, Favorite, pk)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,)
            )
    def shopping_cart(self, request, pk=None):
        return self.add_delete_favorite_shopping_cart(
            request, ShoppingCart, pk)

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
                 .annotate(sum_amount=Sum('amount'))
                 .order_by('name'))
        with StringIO() as file:
            csv.writer(file).writerow(header)
            csv.writer(file).writerows(
                query.values_list('name', 'measurement_unit', 'sum_amount'))

            return HttpResponse(file.getvalue(), headers={
                'Content-Type': 'text/csv',
                'Content-Disposition':
                    'attachment; filename="shopping_cart.csv"',
            })


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filterset_class = IngredientFilterSet
