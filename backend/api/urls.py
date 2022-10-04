from django.urls import path, include
from rest_framework import routers

from api.views import TagsViewSet, IngredientsViewSet, RecipesViewSet

router_v1 = routers.DefaultRouter()

router_v1.register("tags", TagsViewSet, basename="tags")
router_v1.register("ingredients", IngredientsViewSet, basename="ingredients")
router_v1.register("recipes", RecipesViewSet, basename="recipes")


urlpatterns = [
    path("", include(router_v1.urls)),
]
