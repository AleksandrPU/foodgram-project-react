from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.fields import Base64ImageField
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.serializers import UserReadSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'color', 'slug')
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeReadSerializer(serializers.ModelSerializer):
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
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
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

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            instance.tags.set(tags)
        else:
            raise serializers.ValidationError(
                {'errors': 'Теги не указаны.'})
        if 'ingredients' in validated_data:
            for ingredient in instance.ingredients.all():
                ingredient.delete()
            ingredients = validated_data.pop('ingredients')
            for ingredient in ingredients:
                IngredientRecipe.objects.create(
                    recipe=instance,
                    ingredient=ingredient['id'],
                    amount=ingredient['amount']
                )
        else:
            raise serializers.ValidationError(
                {'errors': 'Ингредиенты не указаны.'})
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            context=self.context).to_representation(instance)

    def validate_ingredients(self, value):
        if not value:
            raise serializers.ValidationError(
                {'errors': 'Ингредиенты не указаны.'})
        ids = [item['id'] for item in value]
        if len(set(ids)) != len(ids):
            raise serializers.ValidationError(
                {'errors': 'Рецепт содержит повторяющиеся ингредиенты.'})
        return value

    def validate_tags(self, value):
        if not value:
            raise serializers.ValidationError(
                {'errors': 'Теги не указаны.'})
        if len(set(value)) != len(value):
            raise serializers.ValidationError(
                {'errors': 'Рецепт содержит повторяющиеся теги.'})
        return value
