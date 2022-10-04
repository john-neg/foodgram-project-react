from django.urls import path, include
from rest_framework import routers

from api.views import TagsViewSet

router_v1 = routers.DefaultRouter()

router_v1.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router_v1.urls)),
]
