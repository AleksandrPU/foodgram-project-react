from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

from recipes.models import Recipe


User = get_user_model()


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = [models.UniqueConstraint(
            fields=('user', 'item'), name='unique_user_item')]

    def __str__(self):
        return (f'{self.user.username[:settings.STRING_LENGTH_LIMIT]} '
                f'{self.item.name[:settings.STRING_LENGTH_LIMIT]}')
