from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import UniqueTogetherValidator

from foodgram_backend.constants import RECIPES_MAX_COUNT
from recipes.models import Recipe
from users.models import Subscription

User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True, default=False)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User


class RecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserRecipesSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.BooleanField(read_only=True, default=True)
    recipes_count = serializers.SerializerMethodField(default=0)
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        if limit := self.context["request"].query_params.get('recipes_limit'):
            recipes = Recipe.objects.filter(author=obj)[:int(limit)]
        else:
            recipes = Recipe.objects.filter(author=obj)[:RECIPES_MAX_COUNT]
        return RecipeSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj):
        return Recipe.objects.filter(author=obj).count()


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'following'),
                message='Вы уже подписаны.'
            )
        ]

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Подписаться на самого себя нельзя.')
        return value
