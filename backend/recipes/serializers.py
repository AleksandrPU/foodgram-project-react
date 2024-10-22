from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator

from recipes.fields import Base64ImageField
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag
)
from users.serializers import UserReadSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    """Serializer Tag model."""

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer Ingredient model."""

    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Serializer ingredients of recipe with amount."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
    """Serializer for output recipe."""

    tags = TagSerializer(required=False, many=True)
    author = UserReadSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(read_only=True, many=True)
    is_favorited = serializers.BooleanField(read_only=True, default=False)
    is_in_shopping_cart = serializers.BooleanField(
        read_only=True, default=False)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class IngredientRecipeSerializer(serializers.ModelSerializer):
    """Serializer Ingredient model for create recipe."""

    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Serializer Recipe model for create recipe."""

    ingredients = IngredientRecipeSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time'
        )

    @staticmethod
    def add_ingredients(
            recipe: Recipe,
            ingredients: list
    ) -> None:
        """Add ingredients for create and update recipe."""

        bulk_ingredients = [IngredientRecipe(
            recipe=recipe,
            ingredient=ingredient['id'],
            amount=ingredient['amount']
        ) for ingredient in ingredients]
        IngredientRecipe.objects.bulk_create(bulk_ingredients)

    @transaction.atomic
    def create(self, validated_data: dict) -> Recipe:
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)
        self.add_ingredients(recipe, ingredients)

        return recipe

    @transaction.atomic
    def update(self, instance: Recipe, validated_data: dict) -> Recipe:
        ingredients = validated_data.pop('ingredients')
        super().update(instance, validated_data)

        instance.ingredients.all().delete()

        self.add_ingredients(instance, ingredients)

        return instance

    def to_representation(self, instance: Recipe):
        return RecipeReadSerializer(
            context=self.context).to_representation(instance)

    def validate(self, attrs: dict) -> dict:
        if 'tags' not in attrs:
            raise serializers.ValidationError(
                {'errors': 'Отсутствует поле с тегами.'})
        if 'ingredients' not in attrs:
            raise serializers.ValidationError(
                {'errors': 'Отсутствует поле с ингредиентами.'})
        return attrs

    @staticmethod
    def validate_ingredients(value):
        """Check empty and repeating ingredients."""

        if not value:
            raise serializers.ValidationError(
                {'errors': 'Ингредиенты не указаны.'})
        ids = [item['id'] for item in value]
        if len(set(ids)) != len(ids):
            raise serializers.ValidationError(
                {'errors': 'Рецепт содержит повторяющиеся ингредиенты.'})
        return value

    @staticmethod
    def validate_tags(value):
        """Check empty and repeating tags."""

        if not value:
            raise serializers.ValidationError(
                {'errors': 'Теги не указаны.'})
        if len(set(value)) != len(value):
            raise serializers.ValidationError(
                {'errors': 'Рецепт содержит повторяющиеся теги.'})
        return value


class RecipeShortSerializer(serializers.ModelSerializer):
    """Serializer Recipe model for favorite and shopping_cart actions."""

    image = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')

    def get_image(self, obj: Recipe) -> Optional[str]:
        """Get absolute url for image."""

        if obj.image:
            return self.context["request"].build_absolute_uri(obj.image.url)
        return None


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer Favorite model."""

    class Meta:
        model = Favorite
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в избранное.'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    """Serializer ShoppingCart model."""

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='Рецепт уже добавлен в список закупок.'
            )
        ]
