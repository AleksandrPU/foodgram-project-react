from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet


router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]