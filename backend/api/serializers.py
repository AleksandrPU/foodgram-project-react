from pprint import pprint

from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        # fields = ("email", "id", "username", "first_name", "last_name", "is_subscribed")
        fields = ('email', 'id', 'username', 'first_name', 'last_name')
        model = User


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Tag


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeIngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        fields = ('name', 'measurement_unit', 'amount')
        model = Ingredient

    def get_amount(self, obj):
        # return obj.ingredients.get().amount
        queryset = obj.ingredients.all()
        print('***************')
        pprint(self)
        print('***************')
        pprint(obj)
        pprint(queryset)
        print('***************')
        return queryset


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    # ingredients = RecipeIngredientSerializer(read_only=True, many=True)
    # ingredients = IngredientSerializer(read_only=True, many=True)

    class Meta:
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        model = Recipe
        depth = 1
