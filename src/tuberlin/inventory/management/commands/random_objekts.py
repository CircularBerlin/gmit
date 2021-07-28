from django.core.management.base import BaseCommand
from inventory.models import Material, Objekt

from users.models import CustomUser
import datetime
import string

from random import randrange
import random
from datetime import timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_string(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))


class Command(BaseCommand):
    help = ''

    Objekt.objects.all().delete()

    def handle(self, *args, **options):
        user = CustomUser.objects.first()
        for i in range(0, 1000):
            objekt = Objekt.objects.create(
                created_at=random_date(datetime.datetime(year=2021, month=8, day=1), datetime.datetime(year=2022, month=1, day=1)),
                updated_at=random_date(datetime.datetime(year=2021, month=8, day=1), datetime.datetime(year=2022, month=1, day=1)),
                created_by=user,
                title=random_string(100),
                sold_price_per_unit=randrange(2, 20),
                sold_count=randrange(2, 20),
                eco_cost=randrange(2,20),
                sold_at=random_date(datetime.datetime(year=2021, month=8, day=1), datetime.datetime(year=2022, month=1, day=1))
            )
