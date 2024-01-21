from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from users.serializers import UserSerializer


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
