import base64
import webcolors

from django.core.files.base import ContentFile
from rest_framework import serializers

from .models import Ingredients


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            img_format, img_str = data.split(';base64,')
            ext = img_format.split('/')[-1]
            data = ContentFile(base64.b64decode(img_str), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientsSerializer(serializers.ModelSerializer):
    ingredient_name = serializers.CharField(source='name')

    class Meta:
        model = Ingredients
        fields = ('id', 'ingredient_name')
