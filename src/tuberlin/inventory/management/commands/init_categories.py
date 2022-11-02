from django.core.management.base import BaseCommand
from inventory.models import MaterialCategory


class Command(BaseCommand):
    help = ''

    MaterialCategory.objects.all().delete()

    def handle(self, *args, **options):
        with open('./inventory/fixtures/materials.csv') as file_handle:
            entries = file_handle.read().split('\n')

        for entry in entries:
            print(entry)
            splits = entry.split('\t')
            if len(splits) == 1:
                cat, mat = splits[0], ''
            else:
                cat, mat = splits
            MaterialCategory.objects.get_or_create(text=mat, category=cat)
