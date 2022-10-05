import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredients, Tags, Recipes, Wishlist, Cart
from users.serializers import CustomUserSerializer


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Tags."""

    class Meta:
        model = Tags
        fields = ("id", "name", "color", "slug")


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Ingredients."""

    measurement_unit = serializers.CharField(source="measurement_unit.name")

    class Meta:
        model = Ingredients
        fields = ("id", "name", "measurement_unit")


class RecipesSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Recipes."""

    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_favorited(self, obj):
        """Проверяет, содержится ли данный рецепт в списке избранного."""

        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Wishlist.objects.filter(user_id=user.id, recipe_id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Проверяет, содержится ли данный рецепт в списке покупок."""

        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return Cart.objects.filter(user_id=user.id, recipe_id=obj.id).exists()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            img_format, img_str = data.split(";base64,")
            ext = img_format.split("/")[-1]
            data = ContentFile(base64.b64decode(img_str), name="temp." + ext)

        return super().to_internal_value(data)
