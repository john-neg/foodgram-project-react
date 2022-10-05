from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import IngredientsSearchFilter, RecipesFilter
from .pagination import CustomPageNumberPagination
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import TagsSerializer, IngredientsSerializer, RecipesSerializer
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
    filter_backends = (IngredientsSearchFilter,)
    search_fields = ("^name",)
    pagination_class = None


class RecipesViewSet(viewsets.ModelViewSet):
    """View класс для модели Recipes."""

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    pagination_class = CustomPageNumberPagination
