from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Subscription
from users.paginations import CustomPageNumberPagination
from users.serializers import UserRecipesSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination
    http_method_names = ('get', 'post')

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated:
            queryset = queryset.annotate(is_subscribed=Exists(
                Subscription.objects
                .filter(following=OuterRef('pk'), user=user))
            )
        return queryset

    @action(['get'], detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        super().me(request, *args, **kwargs)
        return self.retrieve(request, *args, **kwargs)

    def activation(self, request, *args, **kwargs):
        pass

    def resend_activation(self, request, *args, **kwargs):
        pass

    def reset_email(self, request, *args, **kwargs):
        pass

    def reset_email_confirm(self, request, *args, **kwargs):
        pass

    def reset_password(self, request, *args, **kwargs):
        pass

    def reset_password_confirm(self, request, *args, **kwargs):
        pass

    def set_email(self, request, *args, **kwargs):
        pass

    def set_username(self, request, *args, **kwargs):
        pass

    def reset_username(self, request, *args, **kwargs):
        pass

    def reset_username_confirm(self, request, *args, **kwargs):
        pass


class SubscribeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, user_id=None):
        ERROR_MESSAGE = 'Ошибка подписки:'

        following = get_object_or_404(User, pk=user_id)
        user = request.user

        if (Subscription.objects
                .filter(user=user, following=following).exists()):
            return Response(
                {'errors': f'{ERROR_MESSAGE} Вы уже подписаны.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            Subscription.objects.create(user=user, following=following)
        except Exception as error:
            return Response(
                {'errors': f'{ERROR_MESSAGE} {error}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(UserRecipesSerializer(following, context={'request': request}).data,
                        status=status.HTTP_201_CREATED)

    def destroy(self, request, user_id=None):
        ERROR_MESSAGE = 'Ошибка отписки:'

        following = get_object_or_404(User, pk=user_id)
        user = request.user

        if obj := Subscription.objects.filter(
                user=user, following=following):
            try:
                obj.delete()
            except Exception as error:
                return Response(
                    {'errors': f'{ERROR_MESSAGE} {error}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': f'{ERROR_MESSAGE} Вы не подписаны.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = UserRecipesSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return (User.objects.filter(following__user=user)
                .annotate(recipes_count=Count('recipes')).order_by('username'))
