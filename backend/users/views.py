from django.contrib.auth import get_user_model
from django.db.models import Count, Exists, OuterRef
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from foodgram_backend.paginations import CustomPageNumberPagination
from users.models import Subscription
from users.serializers import SubscriptionSerializer, UserRecipesSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    http_method_names = ('get', 'post')
    pagination_class = CustomPageNumberPagination

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


class SubscribeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, user_id=None):
        user = request.user
        get_object_or_404(User, pk=user_id)

        serializer = SubscriptionSerializer(
            data={'user': user.id, 'following': user_id},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            UserRecipesSerializer(
                instance.following,
                context={'request': request}
            ).data,
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, user_id=None):
        following = get_object_or_404(User, pk=user_id)
        user = request.user

        if obj := Subscription.objects.filter(
                user=user, following=following):
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Вы не подписаны.'},
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
