from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import (
    CustomUserViewSet,
    SubscriptionsViewSet,
    SubscribeViewSet
)


users = DefaultRouter()
users.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/',
         SubscriptionsViewSet.as_view({'get': 'list'}),
         name='subscriptions'),
    path(r'users/<int:user_id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='subscribe'),
    path('', include(users.urls)),
]
