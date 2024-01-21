from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import validate_username


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'
    ROLES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(
        'Пользователь',
        max_length=150,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    password = models.CharField('Пароль', max_length=150)
    first_name = models.CharField('Имя', max_length=150)
    last_name = models.CharField('Фамилия', max_length=150)
    role = models.CharField(
        'Роль пользователя', choices=ROLES, default=USER, max_length=100)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:settings.STRING_LENGTH_LIMIT]
