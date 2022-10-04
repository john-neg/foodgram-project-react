from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import UserSerializer

User = get_user_model()


# class UsersViewSet(viewsets.ModelViewSet):
#     """View класс для модели User."""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdminOrSuperUser,)
#     lookup_field = "username"
#
#     @action(
#         detail=False,
#         methods=["GET", "PATCH"],
#         permission_classes=(IsOwnerOrModeratorOrAdmin,),
#     )
#     def me(self, request):
#         user = get_object_or_404(User, username=request.user.username)
#         if request.method == "GET":
#             serializer = UserSerializer(instance=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#
#         serializer = UserSerializer(
#             instance=user, data=request.data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         if request.user.is_superuser or request.user.is_staff:
#             serializer.save()
#         else:
#             serializer.save(role=user.role)
#         return Response(serializer.data, status=status.HTTP_200_OK)
