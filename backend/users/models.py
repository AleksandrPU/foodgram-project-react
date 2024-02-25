from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram_backend.constants import (
    EMAIL_MAX_LENGTH,
    STR_LENGTH_LIMIT,
    USERS_FIELD_MAX_LENGTH
)
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
        max_length=USERS_FIELD_MAX_LENGTH,
        unique=True,
        validators=[validate_username]
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=EMAIL_MAX_LENGTH,
        unique=True, blank=False
    )
    password = models.CharField('Пароль', max_length=USERS_FIELD_MAX_LENGTH)
    first_name = models.CharField('Имя', max_length=USERS_FIELD_MAX_LENGTH)
    last_name = models.CharField('Фамилия', max_length=USERS_FIELD_MAX_LENGTH)
    role = models.CharField(
        'Роль пользователя',
        choices=ROLES,
        default=USER,
        max_length=USERS_FIELD_MAX_LENGTH
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:STR_LENGTH_LIMIT]


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='followers'
    )
    following = models.ForeignKey(
        User,
        verbose_name='Подписка',
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique_user_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='no_self_follows'
            )
        ]

    def __str__(self):
        return (f'{self.user.username[:STR_LENGTH_LIMIT]} '
                'подписан на '
                f'{self.following.username[:STR_LENGTH_LIMIT]}')
