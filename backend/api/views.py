from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Cart, Ingredients, RecipeIngredients, Recipes,
                            Tags, Wishlist)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.db.models import Sum

from .filters import IngredientsSearchFilter, RecipesFilter
from .pagination import CustomPageNumberPagination
from .permissions import AdminOrAuthorOrReadOnly
from .reports import cart_report
from .serializers import (CartSerializer, IngredientsSerializer,
                          RecipesSerializer, TagsSerializer,
                          WishlistSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    """Viewset для модели Tags."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Viewset для модели Ingredients."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (IngredientsSearchFilter,)
    search_fields = ("^name",)
    pagination_class = None


class RecipesViewSet(ModelViewSet):
    """Viewset для модели Recipes."""

    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    permission_classes = (AdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipesFilter
    pagination_class = CustomPageNumberPagination

    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {"user": request.user.id, "recipe": pk}
        serializer = serializers(data=data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipes, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=WishlistSerializer
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Wishlist
        )

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=CartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request,
            pk=pk,
            model=Cart,
        )

    @action(
        methods=("GET",),
        permission_classes=(IsAuthenticated,),
        detail=False,
    )
    def download_shopping_cart(self, request):

        user = request.user
        if not user.cart_user.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        ingredients = (
            RecipeIngredients.objects.filter(
                recipe__cart_recipe__user=request.user,
            )
            .values_list(
                "ingredient__name",
                "ingredient__measurement_unit__name",
            )
            .annotate(amount=Sum("amount"))
            .order_by("ingredient__name")
        )

        return cart_report(ingredients)
