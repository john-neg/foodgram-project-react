from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tags(models.Model):
    """Модель для тегов."""

    name = models.CharField(
        "Имя",
        max_length=30,
    )
    color = models.CharField(
        "Цвет",
        max_length=7,
    )
    slug = models.SlugField(
        max_length=10,
        unique=True,
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name


class MeasureUnits(models.Model):
    """Модель для единиц измерения ингредиентов."""

    name = models.CharField(
        "Наименование",
        max_length=20,
        unique=True,
    )

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Модель для ингредиентов."""

    name = models.CharField(
        "Название",
        max_length=50,
        unique=True,
    )
    measurement_unit = models.ForeignKey(
        MeasureUnits,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name="Единицы измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class Recipes(models.Model):
    """Модель для рецептов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор",
    )
    name = models.CharField(
        "Название рецепта",
        max_length=200,
    )
    image = models.ImageField(
        "Изображение", upload_to="recipes/images/", null=True, default=None
    )
    text = models.TextField("Описание рецепта")
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
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления (минут)",
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ("name",)

    def __str__(self):
        return self.name


class RecipesIngredients(models.Model):
    """Модель связей рецептов (Recipes) с ингредиентами (Ingredients)."""

    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        "Количество",
    )

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
