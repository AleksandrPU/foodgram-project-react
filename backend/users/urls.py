import djoser.views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from users.views import UserViewSet, DjoserUserViewSet
from users.views import UserViewSet


# router = DefaultRouter()
# router.register('', UserViewSet, basename='users')
users = DefaultRouter()
users.register("users", UserViewSet, basename='users')


urlpatterns = [
    # path('', include('djoser.urls')),
    path('', include(users.urls)),
    path('', include('djoser.urls.authtoken')),
]
