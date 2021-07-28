from django.core.management.base import BaseCommand
from inventory.models import Material


class Command(BaseCommand):
    help = ''

    Material.objects.all().delete()

    def handle(self, *args, **options):
        with open('./inventory/fixtures/materials.csv') as file_handle:
            entries = file_handle.read().split('\n')

        for entry in entries:
            print(entry)
            cat, mat = entry.split('\t')
            Material.objects.get_or_create(text=mat, category=cat)
