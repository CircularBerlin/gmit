# Generated by Django 3.0.7 on 2022-05-13 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_auto_20211205_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='materialcategory',
            options={'ordering': ('category', 'subcategory'), 'verbose_name': 'Materialkategorie', 'verbose_name_plural': 'Materialkategorien'},
        ),
        migrations.RenameField(
            model_name='materialcategory',
            old_name='text',
            new_name='subcategory',
        ),
    ]
