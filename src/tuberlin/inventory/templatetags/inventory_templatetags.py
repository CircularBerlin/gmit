from django import template
import json
from django.utils.safestring import mark_safe

from inventory.models import MaterialCategory

register = template.Library()


@register.filter
def none_none(val):
    if val is None or val == '':
        return '<Kein Titel angegeben>'
    return val


@register.filter
def dash_none(val):
    if val is None:
        return '-'
    return val


@register.filter
def blank_none(val):
    if val is None:
        return ''
    return val


@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))


@register.simple_tag()
def material_categories():
    return MaterialCategory.objects.order_by('category', 'subcategory').all()


@register.simple_tag()
def distinct_material_categories():
    return MaterialCategory.objects.order_by('category').distinct('category').all()
