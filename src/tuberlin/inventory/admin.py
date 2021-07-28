from django.contrib import admin
from inventory import models


admin.site.register(models.Objekt)
admin.site.register(models.Person)
admin.site.register(models.Material)
