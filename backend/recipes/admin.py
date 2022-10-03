from django.contrib import admin

from .models import Tags, Ingredients, Recipes, MeasureUnits


@admin.register(MeasureUnits)
class MeasureUnitsAdmin(admin.ModelAdmin):
    model = MeasureUnits


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    model = Ingredients
    list_display = (
        "name",
        "measurement_unit",
    )
    empty_value_display = "-отсутствует-"
    search_fields = ("name",)
    list_filter = ("measurement_unit",)
    list_editable = ("measurement_unit",)


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    model = Recipes
    list_display = (
        "name",
        "author",
        "image",
        "text",
        "cooking_time",
    )
    empty_value_display = "-отсутствует-"
    search_fields = ("name",)
    list_editable = ("text", "cooking_time")
    list_filter = ("author",)
    filter_horizontal = ("ingredients", "tags")


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    model = Tags
    list_display = (
        "name",
        "color",
        "slug",
    )
    search_fields = ("name",)
