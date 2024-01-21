from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import RecipeViewSet, TagViewSet, IngredientViewSet


router = DefaultRouter()

router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
