from django_filters import AllValuesMultipleFilter
from django_filters.rest_framework import BooleanFilter, FilterSet
from rest_framework.filters import SearchFilter

from ..recipes.models import Recipes


class IngredientsSearchFilter(SearchFilter):
    """Фильтр поиска по частичному вхождению в начале названия."""

    search_param = "name"


class RecipesFilter(FilterSet):
    """Фильтр рецептор по избранному, автору, списку покупок и тегам."""

    tags = AllValuesMultipleFilter(
        field_name="tags__slug",
    )
    is_favorited = BooleanFilter(
        method="filter_is_favorited",
    )
    is_in_shopping_cart = BooleanFilter(
        method="filter_is_in_shopping_cart",
    )

    class Meta:
        model = Recipes
        fields = ("tags", "author", "is_favorited", "is_in_shopping_cart")

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(wishlist_recipe__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(cart_recipe__user=self.request.user)
        return queryset
