from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=50)
    color = models.CharField('Цвет', max_length=7)
    slug = models.SlugField('Тег', unique=True, max_length=25)

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name[:settings.STRING_LENGTH_LIMIT]


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=150)
    measurement_unit = models.CharField('Единица измерения', max_length=15)

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return (f'{self.name[:settings.STRING_LENGTH_LIMIT]}, '
                f'{self.measurement_unit}')


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Изображение', upload_to='recipe/images/')
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(Ingredient, through='IngredientRecipe', verbose_name='Ингредиенты')
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        help_text='Время приготовления в минутах',
        validators=[MinValueValidator(1)]
    )
    pub_date = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'

    def __str__(self):
        return (f'{self.name[:settings.STRING_LENGTH_LIMIT]}'
                f' от {self.author.username[:settings.STRING_LENGTH_LIMIT]}')


class IngredientRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество', validators=[MinValueValidator(1)])

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=('recipe', 'ingredient'), name='unique_recipe_ingredient')]
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'Ингредиенты для рецепта'

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)
    item = models.ForeignKey(
        Recipe, verbose_name='Рецепт', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'список покупок'
        verbose_name_plural = 'Списки покупок'
        default_related_name = 'shopping'

    def __str__(self):
        return (f'{self.user.username[:settings.STRING_LENGTH_LIMIT]} '
                f'{self.item.name[:settings.STRING_LENGTH_LIMIT]}')
