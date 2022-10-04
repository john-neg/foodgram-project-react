from django.contrib.auth import get_user_model
from rest_framework import viewsets

from api.filters import IngredientSearchFilter
from api.serializers import TagsSerializer, IngredientsSerializer, RecipesSerializer
from recipes.models import Tags, Ingredients, Recipes

User = get_user_model()


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """View класс для модели Tags."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """View класс для модели Ingredients."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientSearchFilter,)
    search_fields = ("^name",)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """View класс для модели Recipes."""

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
