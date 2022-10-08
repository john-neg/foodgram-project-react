import csv
import shutil

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from backend import settings
from recipes.models import (Cart, Ingredients, MeasureUnits, RecipeIngredients,
                            Recipes, RecipeTags, Tags, Wishlist)
from users.models import Follow, User


class Command(BaseCommand):
    help = "Загружает данные из папки data в базу данных"

    def handle(self, *args, **options):

        with open("data/users.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            User.objects.all().delete()
            print("Загружаю данные в Users")
            for row in reader:
                user = User(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    first_name=row[3],
                    last_name=row[4],
                    is_active=row[6],
                    is_staff=row[7],
                    is_superuser=row[8],
                )
                user.set_password(row[5])
                user.save()

        with open("data/follow.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            Follow.objects.all().delete()
            print("Загружаю данные в Follow")
            for row in reader:
                follow = Follow(
                    id=row[0],
                    user=get_object_or_404(User, pk=row[1]),
                    author=get_object_or_404(User, pk=row[2]),
                )
                follow.save()

        with open("data/ingredients.csv") as file:
            reader = csv.reader(file)
            Ingredients.objects.all().delete()
            MeasureUnits.objects.all().delete()
            print("Загружаю данные в Ingredients и MeasureUnits")
            for count, row in enumerate(reader):
                measurement_unit, _ = MeasureUnits.objects.get_or_create(
                    name=row[-1],
                )
                ingredient = Ingredients(
                    id=count + 1,
                    name=row[0],
                    measurement_unit_id=measurement_unit.id,
                )
                ingredient.save()

        with open("data/tags.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            Tags.objects.all().delete()
            print("Загружаю данные в Tags")
            for row in reader:
                tag = Tags(
                    id=row[0],
                    name=row[1],
                    color=row[2],
                    slug=row[3],
                )
                tag.save()

        with open("data/recipes.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            Recipes.objects.all().delete()
            print("Загружаю данные в Recipes")
            for row in reader:
                recipes = Recipes(
                    id=row[0],
                    name=row[1],
                    image=row[2],
                    text=row[3],
                    cooking_time=row[4],
                    author_id=row[5],
                )
                recipes.save()

        shutil.rmtree(settings.MEDIA_ROOT + "/images", ignore_errors=True)
        shutil.copytree(
            "data/images/",
            settings.MEDIA_ROOT + "/images",
        )

        with open("data/recipetags.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            RecipeTags.objects.all().delete()
            print("Загружаю данные в RecipeTags")
            for row in reader:
                tags = RecipeTags(
                    id=row[0],
                    recipe_id=row[1],
                    tag_id=row[2],
                )
                tags.save()

        with open("data/recipeingredients.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            RecipeIngredients.objects.all().delete()
            print("Загружаю данные в RecipeIngredients")
            for row in reader:
                ingredients = RecipeIngredients(
                    id=row[0],
                    recipe_id=row[1],
                    ingredient_id=row[2],
                    amount=row[3],
                )
                ingredients.save()

        with open("data/wishlist.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            Wishlist.objects.all().delete()
            print("Загружаю данные в Wishlist")
            for row in reader:
                wishlist = Wishlist(
                    id=row[0],
                    recipe_id=row[1],
                    user_id=row[2],
                )
                wishlist.save()

        with open("data/cart.csv") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            Cart.objects.all().delete()
            print("Загружаю данные в Cart")
            for row in reader:
                cart = Cart(
                    id=row[0],
                    recipe_id=row[1],
                    user_id=row[2],
                )
                cart.save()

        print("Данные успешно загружены")
