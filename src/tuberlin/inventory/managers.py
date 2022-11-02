from django.db.models import Manager


class BaseModelManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class PeopleManager(BaseModelManager):
    pass


class AllOfferManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter()


class PendingOfferManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(offer_status__text='pending')


class AcceptedOfferManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(offer_status__text='accepted')


class RejectedOfferManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(offer_status__text='rejected')


class AllObjektManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(archived_at__isnull=True)


class WarehouseObjektManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(sold_at__isnull=True,
                                             archived_at__isnull=True)


class AvailableObjektManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(available_on_restado=True,
                                             sold_at__isnull=True,
                                             archived_at__isnull=True)


class SoldObjektManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(archived_at__isnull=True, sold_at__isnull=False)


class ArchivedObjektManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(archived_at__isnull=False)


class DeletedBaseModelManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=False)


class RestadoObjektManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().filter(available_on_restado=True,
                                             # sold_at__isnull=True,
                                             archived_at__isnull=True)


class StatusManager(BaseModelManager):
    def get_queryset(self):
        return super().get_queryset().order_by('ordering')
