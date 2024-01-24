from django.contrib.auth import get_user_model
# todo
# from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


User = get_user_model()


class UserReadSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.following.filter(user=user).exists()
        return False


# todo
class UserAfterCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


# todo
# class UserRegistrationSerializer(UserCreateSerializer):
class UserRegistrationSerializer(serializers.ModelSerializer):

    # class Meta(UserCreateSerializer.Meta):
    class Meta:
        model = User
        # todo
        # fields = ('url', 'id', 'email', 'name', 'last_name', 'account_address', 'password', )
        # fields = ('id', 'email', 'username', 'first_name', 'last_name', 'password')
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    # todo
    def to_representation(self, instance):
        return UserAfterCreateSerializer(
            context=self.context).to_representation(instance)
