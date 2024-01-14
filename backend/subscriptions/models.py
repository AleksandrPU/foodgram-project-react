from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


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
        return (f'{self.user.username[:settings.STRING_LENGTH_LIMIT]} '
                'подписан на '
                f'{self.following.username[:settings.STRING_LENGTH_LIMIT]}')
