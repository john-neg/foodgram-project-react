# Generated by Django 3.2.16 on 2022-10-08 14:03

import colorfield.fields

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredients_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredients',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, message='Минимальное количество - 1'), django.core.validators.MaxValueValidator(32767, message='Максимальное количество - 32767')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='tags',
            name='color',
            field=colorfield.fields.ColorField(default='#FF0000', image_field=None, max_length=18, samples=None, verbose_name='Цвет'),
        ),
    ]
