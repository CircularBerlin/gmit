# Generated by Django 3.0.7 on 2021-11-25 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='objekt',
            name='sold_count',
            field=models.FloatField(null=True),
        ),
    ]
