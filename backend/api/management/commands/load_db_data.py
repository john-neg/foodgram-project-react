import csv

from django.core.management import BaseCommand
from django.shortcuts import get_object_or_404

from recipes.models import Ingredients, Recipes, MeasureUnits, Tags
from users.models import User, Follow


class Command(BaseCommand):
    help = "Загружает данные из папки data в базу данных"

    def handle(self, *args, **options):

        with open("../data/users.csv") as file:
            reader = csv.reader(file)
            next(reader)
            User.objects.all().delete()
            print(f"Загружаю данные в Users")
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

        with open("../data/follow.csv") as file:
            reader = csv.reader(file)
            next(reader)
            Follow.objects.all().delete()
            print(f"Загружаю данные в Follow")
            for row in reader:
                follow = Follow(
                    id=row[0],
                    user=get_object_or_404(User, pk=row[1]),
                    author=get_object_or_404(User, pk=row[2]),
                )
                follow.save()

        with open("../data/ingredients.csv") as file:
            reader = csv.reader(file)
            Ingredients.objects.all().delete()
            MeasureUnits.objects.all().delete()
            print(f"Загружаю данные в Ingredients и MeasureUnits")
            for row in reader:
                measurement_unit, _ = MeasureUnits.objects.get_or_create(
                    name=row[-1],
                )
                ingredient = Ingredients(
                    name=row[0], measurement_unit_id=measurement_unit.id
                )
                ingredient.save()

        with open("../data/tags.csv") as file:
            reader = csv.reader(file)
            next(reader)
            Tags.objects.all().delete()
            print(f"Загружаю данные в Tags")
            for row in reader:
                tag = Tags(
                    id=row[0],
                    name=row[1],
                    color=row[2],
                    slug=row[3],
                )
                tag.save()

        print("Данные успешно загружены")
