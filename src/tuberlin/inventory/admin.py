from django.contrib import admin
from inventory import models


# admin.site.register(models.Objekt)
# admin.site.register(models.Person)

class MaterialCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'subcategory')
        }),
    )

    list_display = ('category', 'subcategory')
    list_filter = ('category',)

admin.site.register(models.MaterialCategory, MaterialCategoryAdmin)

