from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from inventory.managers import (BaseModelManager,
                                PendingOfferManager,
                                AcceptedOfferManager,
                                RejectedOfferManager,
                                AllObjektManager,
                                WarehouseObjektManager,
                                AvailableObjektManager,
                                SoldObjektManager,
                                ArchivedObjektManager,
                                DeletedBaseModelManager,
                                RestadoObjektManager,
                                StatusManager)
from users.models import CustomUser


class BaseModel(models.Model):
    objects = BaseModelManager()
    deleted_objects = DeletedBaseModelManager()

    updated_at = models.DateTimeField(default=now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(default=now)
    created_by = models.ForeignKey(CustomUser,
                                   null=True,
                                   blank=True,
                                   on_delete=models.SET_NULL)

    class Meta:
        abstract = True

    def save(self,
             force_insert=False,
             force_update=False,
             using=None,
             update_fields=None):
        self.updated_at = now()
        super(BaseModel, self).save(force_insert, force_update, using, update_fields)


class Image(BaseModel):
    filename = models.CharField(max_length=2000)


class MaterialCategory(BaseModel):
    class Meta:
        verbose_name = 'Materialkategorie'
        verbose_name_plural = 'Materialkategorien'
        ordering = ('category', 'subcategory')

    category = models.CharField(max_length=200,
                                default='',
                                null=False,
                                verbose_name='Kategorie',
                                help_text='Kategorie (zb: Glas, Holz, Metall')

    subcategory = models.CharField(max_length=200,
                                   null=True,
                                   blank=True)

    @property
    def related_subcategories(self):
        subcategories = MaterialCategory.objects.filter(category=self.category).order_by('subcategory').all()
        return subcategories

    def __str__(self):
        if self.subcategory:
            return "{} ({})".format(self.category, self.subcategory)
        else:
            return self.category


class Status(BaseModel):
    class Meta:
        abstract = True

    objects = StatusManager()

    text = models.CharField(max_length=40,
                            null=False,
                            blank=False)

    display_name = models.CharField(max_length=200,
                                    null=False,
                                    blank=False)

    help_text = models.TextField(null=True, blank=True)
    ordering = models.IntegerField(default=0)

    def __str__(self):
        return self.display_name


class OfferStatus(Status):
    pass


class Condition(models.TextChoices):
    NEW = 'NEW', _('Neu/Neuwertig')
    USED = 'USED', _('Gebraucht')
    VERY_USED = 'VERY_USED', _('Sehr gebraucht')


class Unit(models.TextChoices):
    QUADRATMETER = 'QUADRATMETER', _('Quadratmeter')
    LFM = 'LFM', _('LFM')
    STUECK = 'STUECK', _('Stück')
    LITER = "LITER", _('Liter')


class ProviderType(models.TextChoices):
    PRIVATE = 'PRIVATE', _('Privat')
    COMMERCIAL = 'COMMERCIAL', _('Kommerziell')


class ImportPreferences(models.TextChoices):
    PICKUP = 'PICKUP', _('Abholung')
    DELIVERY = 'DELIVERY', _('Lieferung an Material Mafia')


class Offer(BaseModel):
    class Meta:
        verbose_name = 'Angebot'
        verbose_name_plural = 'Angebote'
        ordering = ['-updated_at']

    objects = BaseModelManager()
    pending_objects = PendingOfferManager()
    rejected_objects = RejectedOfferManager()
    accepted_objects = AcceptedOfferManager()

    provider_type = models.CharField(max_length=100,
                                     choices=ProviderType.choices,
                                     default=ProviderType.PRIVATE,
                                     verbose_name='provider_type')
    provider_description = models.CharField(max_length=1000, null=True, blank=True)

    email = models.EmailField(blank=False)

    offer_status = models.ForeignKey(OfferStatus,
                                     default=1,
                                     on_delete=models.PROTECT)

    images = models.ManyToManyField(Image,
                                    blank=True,
                                    related_name='offer_images')
    thumbnail_image = models.ForeignKey(Image,
                                        null=True,
                                        on_delete=models.SET_NULL,
                                        related_name='offer_thumbnail_image')

    message = models.TextField(null=True,
                               blank=True,
                               verbose_name='Nachricht')

    import_preferences = models.TextField(max_length=9,
                                          null=True,
                                          choices=ImportPreferences.choices,
                                          default=ImportPreferences.PICKUP,
                                          verbose_name='Lieferpräferenzen')

    import_at = models.DateTimeField(null=True,
                                     blank=True)

    @property
    def recent_offer_status(self):
        statuslog = self.offerstatuslog_set.order_by('-created_at').first()
        if statuslog:
            return statuslog.offer_status
        return None

    @property
    def recent_offer_status_time(self):
        statuslog = self.offerstatuslog_set.order_by('-created_at').first()
        if statuslog and statuslog.created_at:
            # assert self.offer_status == statuslog.offer_status
            return statuslog.created_at.strftime('%d %b %Y, %H:%M')
        return None


class Objekt(BaseModel):
    class Meta:
        verbose_name = 'Objekt'
        verbose_name_plural = 'Objekte'
        ordering = ['-updated_at']

    objects = models.Manager()
    all_objects = AllObjektManager()
    warehouse_objects = WarehouseObjektManager()
    available_objects = AvailableObjektManager()
    sold_objects = SoldObjektManager()
    archived_objects = ArchivedObjektManager()

    restado_objects = RestadoObjektManager()

    title = models.CharField(max_length=200,
                             verbose_name='Haupttitel')

    material = models.ManyToManyField(MaterialCategory, verbose_name='Materialkategorien')

    unit = models.CharField(max_length=200,
                            null=True,
                            choices=Unit.choices,
                            default=Unit.QUADRATMETER,
                            verbose_name='Einheit')

    approximate = models.BooleanField(default=False,
                                      verbose_name='Messung ist ungefähr')

    width = models.FloatField(null=True,
                              blank=True,
                              default=None,
                              verbose_name='Breite oder Durchmesser (cm)')

    length = models.FloatField(null=True,
                               blank=True,
                               default=None,
                               verbose_name='Länge')

    height = models.FloatField(null=True,
                               blank=True,
                               default=None,
                               verbose_name='Höhe (cm)')

    depth = models.FloatField(null=True,
                              blank=True,
                              default=None,
                              verbose_name='Tiefe (cm)')

    treatment_notes = models.TextField(null=True,
                                       blank=True,
                                       verbose_name='Behandlungshinweise')

    mass = models.FloatField(null=True,
                             blank=True,
                             default=None,
                             verbose_name='Gewicht (kg)')

    count = models.FloatField(null=True,
                              blank=True,
                              default=0.0,
                              verbose_name='Stückanzahl')

    condition = models.CharField(max_length=9,
                                 null=True,
                                 choices=Condition.choices,
                                 default=Condition.NEW,
                                 verbose_name='Zustand')

    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Beschreibung')

    images = models.ManyToManyField(Image,
                                    blank=True,
                                    related_name='objekt_images')
    thumbnail_image = models.ForeignKey(Image,
                                        null=True,
                                        on_delete=models.SET_NULL,
                                        related_name='objekt_thumbnail_image')

    price = models.FloatField(null=True,
                              blank=True,
                              verbose_name='Verkaufspreis (€/Einheit)')

    reference_price = models.FloatField(null=True,
                                        blank=True,
                                        verbose_name='Referenzpreis (€/Einheit)')

    eco_cost = models.FloatField(null=True,
                                 blank=True,
                                 verbose_name='Ecocost (€/Einheit)')

    available_on_restado = models.BooleanField(default=False)

    knowledge_base = models.BooleanField(default=False)

    sold_at = models.DateTimeField(null=True)
    sold_count = models.FloatField(null=True)
    sold_price_per_unit = models.FloatField(null=True)
    sold_by = models.ForeignKey(CustomUser, null=True, on_delete=models.PROTECT, related_name='sold_by')

    partial_sale_parent = models.ForeignKey('Objekt',
                                            null=True,
                                            blank=True,
                                            on_delete=models.PROTECT,
                                            related_name='partial_sale_children')

    archived_at = models.DateTimeField(null=True, blank=True)

    offer = models.ForeignKey(to=Offer,
                              null=True,
                              on_delete=models.SET_NULL)

    cloned_from = models.ForeignKey(to='Objekt',
                                    null=True,
                                    related_name='cloned_from_children',
                                    on_delete=models.PROTECT)

    def __str__(self):
        return "{}".format(self.title)

    def sell(self, sold_count, sold_price_per_unit, sold_by):
        if sold_price_per_unit < 0:
            assert False

        if self.count is None or sold_count < self.count:
            if self.count is not None:
                self.count = self.count - sold_count
                self.save()

            cloned_objekt = Objekt.objects.create(
                title=self.title,
                count=0,
                unit=self.unit,
                width=self.width,
                length=self.length,
                height=self.height,
                depth=self.depth,
                condition=self.condition,
                mass=self.mass,
                treatment_notes=self.treatment_notes,
                description=self.description,
                price=self.price,
                cloned_from=None,
                offer=self.offer,
                reference_price=self.reference_price,
                eco_cost=self.eco_cost,
                available_on_restado=False
            )

            cloned_objekt.sold_at = now()
            cloned_objekt.sold_by = sold_by
            cloned_objekt.sold_count = sold_count
            cloned_objekt.sold_price_per_unit = sold_price_per_unit
            cloned_objekt.partial_sale_parent = self

            for material in self.material.all():
                cloned_objekt.material.add(material)

            for image in self.images.all():
                cloned_objekt.images.add(image)

            cloned_objekt.save()
        elif sold_count == self.count:
            self.sold_at = now()
            self.sold_by = sold_by
            self.sold_count = sold_count
            self.sold_price_per_unit = sold_price_per_unit
            self.partial_sale_parent = None
            self.available_on_restado = False
            self.count = 0
            self.save()


class OfferStatusLog(BaseModel):
    offer = models.ForeignKey(Offer, null=False, on_delete=models.CASCADE)
    offer_status = models.ForeignKey(OfferStatus, null=False, on_delete=models.CASCADE)


class Comment(BaseModel):
    class Meta:
        verbose_name = 'Bemerkung'
        verbose_name_plural = 'Bemerkungen'

    objekt = models.ForeignKey(Objekt,
                               null=True,
                               on_delete=models.SET_NULL,
                               related_name='comments')
    text = models.TextField(null=True,
                            blank=True)

    def __str__(self):
        return "{} on {}".format(self.text, self.offer)


class Person(BaseModel):
    email = models.EmailField(null=False,
                              unique=True,
                              verbose_name='Email')

    notes = models.TextField(null=True,
                             blank=True,
                             verbose_name='Notiz')

    class Meta:
        verbose_name_plural = 'Personen'

    def __str__(self):
        return self.email
