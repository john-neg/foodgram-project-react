from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tags(models.Model):
    """Модель для тегов."""

    name = models.CharField(max_length=30)
    color = models.CharField(max_length=6)
    slug = models.SlugField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class IngredientsMeasureUnit(models.Model):
    """Модель для единиц измерения ингредиентов."""

    name = models.CharField(max_length=20, unique=True)


class Ingredients(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(max_length=50, unique=True)
    measurement_unit = models.ForeignKey(
        IngredientsMeasureUnit, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)


class Recipes(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор"
    )
    name = models.CharField(max_length=200, verbose_name="Название рецепта")
    image = models.ImageField(
        upload_to="recipes/images/", null=True, default=None
    )
    text = models.TextField(verbose_name="Описание рецепта")
    ingredients = models.ManyToManyField(
        Ingredients,
        through="RecipesIngredients",
        related_name="recipes",
        verbose_name="Ингридиенты",
    )
    tags = models.ManyToManyField(
        Tags,
        through="RecipesTags",
        related_name="recipes",
        verbose_name="Теги",
    )
    cooking_time = models.PositiveIntegerField

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("name",)


class RecipesIngredients(models.Model):
    """Модель связей рецептов (Recipes) с ингредиентами (Ingredients)."""

    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_relationships",
                fields=["recipe", "ingredient"],
            ),
        ]


class RecipesTags(models.Model):
    """Модель связей рецептов (Recipes) с тегами (Tags)."""

    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_relationships",
                fields=["recipe", "tag"],
            ),
        ]
