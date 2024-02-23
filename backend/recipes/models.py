from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from foodgram_backend.constants import (
    COLOR_MAX_LENGTH,
    INGREDIENT_MAX_LENGTH,
    RECIPE_MAX_LENGTH,
    STR_LENGTH_LIMIT,
    TAG_MAX_LENGTH,
    UNIT_MAX_LENGTH,
    VALIDATOR_MIN_VALUE
)

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название', max_length=TAG_MAX_LENGTH, unique=True)
    color = models.CharField(
        'Цвет', max_length=COLOR_MAX_LENGTH, default='#0f0f0f', unique=True)
    slug = models.SlugField('Тег', unique=True, max_length=TAG_MAX_LENGTH)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:STR_LENGTH_LIMIT]


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=INGREDIENT_MAX_LENGTH)
    measurement_unit = models.CharField(
        'Единица измерения', max_length=UNIT_MAX_LENGTH)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return (f'{self.name[:STR_LENGTH_LIMIT]}, '
                f'{self.measurement_unit}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=RECIPE_MAX_LENGTH)
    image = models.ImageField('Изображение', upload_to='recipe/images/')
    text = models.TextField('Описание')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Время приготовления в минутах',
        validators=[MinValueValidator(VALIDATOR_MIN_VALUE)]
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'

    def __str__(self):
        return (f'{self.name[:STR_LENGTH_LIMIT]}'
                f' от {self.author.username[:STR_LENGTH_LIMIT]}')


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=[MinValueValidator(VALIDATOR_MIN_VALUE)])

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('recipe', 'ingredient'), name='unique_recipe_ingredient')]
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'избранное'
        verbose_name_plural = 'Избранное'
        default_related_name = 'favorites'
        constraints = [models.UniqueConstraint(
            fields=('user', 'recipe'), name='unique_user_item')]

    def __str__(self):
        return (f'{self.user.username[:STR_LENGTH_LIMIT]} '
                f'{self.recipe.name[:STR_LENGTH_LIMIT]}')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping'

    def __str__(self):
        return (f'{self.user.username[:STR_LENGTH_LIMIT]} '
                f'{self.recipe.name[:STR_LENGTH_LIMIT]}')
