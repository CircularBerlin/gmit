from django.shortcuts import reverse
from django.template.loader import get_template
from rest_framework import serializers
from inventory.models import Objekt, Image, Person, Offer, Material
from django.template.defaultfilters import date as _date


class PersonSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    link = serializers.SerializerMethodField('_link')

    updated_at_display = serializers.SerializerMethodField('_updated_at_display')
    created_at_display = serializers.SerializerMethodField('_created_at_display')

    def _updated_at_display(self, instance):
        if instance and instance.updated_at:
            return _date(instance.updated_at, 'd. N Y H:i')
        return ''

    def _created_at_display(self, instance):
        if instance and instance.created_at:
            return _date(instance.created_at, 'd. N Y H:i')
        return ''

    def _thumbnail(self, instance):
        template = get_template('thumbnail_td.html')
        return template.render({
            'offer': instance
        })

    def _link(self, instance):
        if instance:
            return '<a href="{}">{}</a>'.format(
                reverse('inventory_person', args=(instance.id,)),
                instance.name
            )
        return None

    class Meta:
        model = Person
        fields = [
            'id',
            'link',
            'email',
            'phone_number',
            'name',
            'notes',
            'updated_at_display',
            'created_at_display',
            'created_at',
            'updated_at'
        ]


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    filename = serializers.CharField(read_only=True)
    thumbnail = serializers.SerializerMethodField('_thumbnail')

    def _thumbnail(self, instance):
        if instance:
            for oi in instance.objekt_images.all():
                if oi.thumbnail_image == instance:
                    return True
            return False


    class Meta:
        model = Image
        fields = [
            'id',
            'filename',
            'thumbnail'
        ]


class OfferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    link = serializers.SerializerMethodField('_link')
    offer_status_text = serializers.SerializerMethodField('_offer_status_text')
    recent_offer_status_time = serializers.SerializerMethodField('_recent_offer_status_time')
    thumbnail = serializers.SerializerMethodField('_thumbnail')

    updated_at_display = serializers.SerializerMethodField('_updated_at_display')
    created_at_display = serializers.SerializerMethodField('_created_at_display')

    def _updated_at_display(self, instance):
        if instance and instance.updated_at:
            return _date(instance.updated_at, 'd. N Y H:i')
        return ''

    def _created_at_display(self, instance):
        if instance and instance.created_at:
            return _date(instance.created_at, 'd. N Y H:i')
        return ''

    def _thumbnail(self, instance):
        template = get_template('thumbnail_td.html')
        return template.render({
            'offer': instance
        })

    def _recent_offer_status_time(self, instance):
        if instance:
            return instance.recent_offer_status_time

    def _offer_status_text(self, instance):
        if instance and instance.offer_status:
            return instance.offer_status.display_name
        return None

    def _link(self, instance):
        if instance:
            return '<a href="{}">{}</a>'.format(
                reverse('inventory_offer', args=(instance.id,)),
                instance.message
            )
        return None

    class Meta:
        model = Offer
        fields = [
            'id',
            'link',
            'message',
            'updated_at_display',
            'thumbnail',
            'offer_status_text',
            'recent_offer_status_time',
            'person_name',
            'created_at_display',
            'updated_at',
            'created_at'
        ]


class ObjektSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    material_text = serializers.SerializerMethodField('_material_text')

    link = serializers.SerializerMethodField('_link')
    # person_link = serializers.SerializerMethodField('_person_link')

    thumbnail = serializers.SerializerMethodField('_thumbnail')
    description = serializers.SerializerMethodField('_description')

    updated_at_display = serializers.SerializerMethodField('_updated_at_display')
    created_at_display = serializers.SerializerMethodField('_created_at_display')
    sold_at_display = serializers.SerializerMethodField('_sold_at_display')

    def _updated_at_display(self, instance):
        if instance and instance.updated_at:
            return _date(instance.updated_at, 'd. N Y H:i')
        return ''

    def _sold_at_display(self, instance):
        if instance and instance.sold_at:
            return _date(instance.sold_at, 'd. N Y H:i')
        return ''

    def _created_at_display(self, instance):
        if instance and instance.created_at:
            return _date(instance.created_at, 'd. N Y H:i')
        return ''

    def _description(self, instance):
        if instance and instance.description:
            if len(instance.description) > 100:
                return instance.description[0:100] + '...'
            else:
                return instance.description
        return None

    def _thumbnail(self, instance):
        template = get_template('thumbnail_td.html')
        return template.render({
            'objekt': instance
        })

    def _material_text(self, instance):
        if instance:
            return "<br>".join([str(m) for m in instance.material.all()])
        return None

    def _link(self, instance):
        if instance:
            if instance.title and instance.title != '':
                return '<a href="{}">{}</a>'.format(
                    reverse('inventory_objekt', args=(instance.id,)),
                    instance.title
                )
            else:
                return '<a href="{}">{}</a>'.format(
                    reverse('inventory_objekt', args=(instance.id,)),
                    '(Unbekannt)'
                )
        return None

    class Meta:
        model = Objekt
        fields = [
            'link',

            'id',
            'title',

            'material_text',

            'width',
            'height',
            'depth',
            'mass',
            'count',
            'description',
            'treatment_notes',
            'condition',
            'created_at_display',
            'updated_at',
            'created_at',
            'deleted_at',
            'updated_at_display',
            'archived_at',
            'sold_at',
            'price',
            'thumbnail',
            'sold_at_display',
            'sold_by',
            'sold_price_per_unit',
            'sold_count'
        ]


class RestadoObjektSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    def _material(self, instance):
        if instance:
            return [{
                'id': mat.id,
                'text': mat.text,
                'category': mat.category
            } for mat in instance.material.all()]
        return []

    material = serializers.SerializerMethodField('_material')

    class Meta:
        model = Objekt
        fields = [
            'id',

            'material',

            'title',

            'unit',
            'width',
            'height',
            'depth',
            'mass',
            'count',
            'description',
            'treatment_notes',
            'condition',
            'created_at',
            'price',

            'images'
        ]


class RestadoMaterialSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Material
        fields = [
            'id',
            'category',
            'text',
            'created_at',
            'updated_at'
        ]
