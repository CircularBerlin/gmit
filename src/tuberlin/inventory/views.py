import uuid
import os
import datetime
import csv

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, reverse, get_object_or_404
from django.utils.timezone import now
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.template.loader import get_template
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models.functions import TruncMonth, ExtractMonth

from rest_framework import filters
from storages.backends.s3boto3 import S3Boto3Storage

from inventory.forms import OfferForm, ObjektForm, PersonForm
from inventory.models import Objekt, Offer, Comment, Image, Status, OfferStatus, OfferStatusLog, Person, MaterialCategory
from inventory.serializers import ObjektSerializer, RestadoObjektSerializer, RestadoMaterialSerializer, \
    PersonSerializer, OfferSerializer
from inventory.utils import convert_float

from rest_framework import viewsets


@login_required
def objekt_dashboard(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_all_objekts.html',
                  context={
                      'tab_stub': 'all',
                      'menu_stub': 'offers'
                  })


@login_required
def people_dashboard(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_people.html',
                  context={
                      'tab_stub': 'people',
                      'menu_stub': 'people'
                  })


@login_required
def objekt_dashboard_offers(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_all_offers.html',
                  context={
                      'tab_stub': 'all',
                      'menu_stub': 'offers'
                  })


@login_required
def objekt_dashboard_pending(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_pending.html',
                  context={
                      'tab_stub': 'pending',
                      'menu_stub': 'offers'
                  })


@login_required
def objekt_dashboard_accepted(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_accepted.html',
                  context={
                      'tab_stub': 'accepted',
                      'menu_stub': 'offers'
                  })


@login_required
def objekt_dashboard_rejected(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_rejected.html',
                  context={
                      'tab_stub': 'rejected',
                      'menu_stub': 'offers'
                  })


@login_required
def objekt_dashboard_materials(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_materials.html',
                  context={
                      'tab_stub': 'all',
                      'menu_stub': 'materials'
                  })


@login_required
def objekt_dashboard_warehouse(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_warehouse.html',
                  context={
                      'tab_stub': 'warehouse',
                      'menu_stub': 'materials'
                  })


@login_required
def objekt_dashboard_available(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_available.html',
                  context={
                      'tab_stub': 'available',
                      'menu_stub': 'materials'
                  })


@login_required
def objekt_dashboard_sold(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_sold.html',
                  context={
                      'tab_stub': 'sold',
                      'menu_stub': 'materials'
                  })


@login_required
def objekt_dashboard_archived(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_archived.html',
                  context={
                      'tab_stub': 'archived',
                      'menu_stub': 'materials'
                  })


@login_required
def objekt_dashboard_deleted(request: HttpRequest) -> HttpResponse:
    return render(request=request,
                  template_name='dashboards/dashboard_deleted.html',
                  context={
                      'tab_stub': 'deleted',
                      'menu_stub': 'materials'
                  })


class PersonAPIViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.filter(deleted_at__isnull=True).order_by('id')
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


OBJEKT_SEARCH_FIELDS = [
    'title',
    'status__text',
]


class OfferAllAPIViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.order_by('id')
    serializer_class = OfferSerializer

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter
    ]
    search_fields = ['email']


class OfferPendingAPIViewSet(viewsets.ModelViewSet):
    queryset = Offer.pending_objects.all().order_by('id')
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class OfferAcceptedAPIViewSet(viewsets.ModelViewSet):
    queryset = Offer.accepted_objects.all().order_by('id')
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class OfferRejectedAPIViewSet(viewsets.ModelViewSet):
    queryset = Offer.rejected_objects.all().order_by('id')
    serializer_class = OfferSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ObjektAllAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.all_objects.all().order_by('id')
    serializer_class = ObjektSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = OBJEKT_SEARCH_FIELDS

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ObjektWarehouseAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.warehouse_objects.all().order_by('id')
    serializer_class = ObjektSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = OBJEKT_SEARCH_FIELDS

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ObjektAvailableAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.available_objects.all().order_by('id')
    serializer_class = ObjektSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = OBJEKT_SEARCH_FIELDS

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ObjektSoldAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.sold_objects.all().order_by('id')
    serializer_class = ObjektSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = OBJEKT_SEARCH_FIELDS

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ObjektArchivedAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.archived_objects.all().order_by('id')
    serializer_class = ObjektSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = OBJEKT_SEARCH_FIELDS

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ObjektDeletedAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.deleted_objects.all().order_by('id')
    serializer_class = ObjektSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = OBJEKT_SEARCH_FIELDS

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class RestadoObjektAPIViewSet(viewsets.ModelViewSet):
    queryset = Objekt.restado_objects.all().order_by('id')
    serializer_class = RestadoObjektSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class RestadoMaterialAPIViewSet(viewsets.ModelViewSet):
    queryset = MaterialCategory.objects.all().order_by('id')
    serializer_class = RestadoMaterialSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


def offer_transform(request: HttpRequest, offer_pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=offer_pk)
    objekt = Objekt.objects.create()
    objekt.description = offer.message

    if offer.images.count():
        objekt.images.add(offer.images.all()[0])

    objekt.offer = offer
    objekt.save()

    return HttpResponseRedirect(redirect_to=reverse('inventory_objekt', args=(objekt.id,)))


def offer_delete(request: HttpRequest, offer_pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=offer_pk)
    offer.delete()

    return HttpResponseRedirect(redirect_to=reverse('inventory_objekt_dashboard_offers'))


def offer_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        offer_form = OfferForm(request.POST, request.FILES)
        if offer_form.is_valid():
            offer = offer_form.save()
            email = request.POST['email'].lower()

            person = Person.objects.filter(email=email).first()
            if not person:
                person = Person.objects.create(
                    email=email
                )

            person.save()

            return render(request=request,
                          template_name='objekt/pages/offer_created.html',
                          context={
                              'offer': offer
                          })

    else:
        offer_form = OfferForm()

    return render(request=request,
                  template_name='objekt/pages/offer_create.html',
                  context={
                      'offer_form': offer_form,
                  })


@login_required
def objekt_create(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        objekt_form = ObjektForm(request.POST, request.FILES)
        if objekt_form.is_valid():
            objekt = objekt_form.save()
            objekt.offer_status_id = 3
            objekt.save()

            objekt.material.clear()
            categories = request.POST.getlist('subcategory[]')
            for category in categories:
                if category != '':
                    objekt.material.add(MaterialCategory.objects.get(pk=int(category)))

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(objekt).pk,
                object_id=objekt.pk,
                object_repr=str(objekt),
                change_message="Material wurde erstellt",
                action_flag=CHANGE)

            return HttpResponseRedirect(redirect_to=reverse('inventory_objekt', args=(objekt.id,)))
    else:
        objekt_form = ObjektForm()

    objekts = Objekt.objects.filter(knowledge_base=True).order_by('title')

    return render(request=request,
                  template_name='objekt/pages/objekt_create.html',
                  context={
                      'objekt_form': objekt_form,
                      'objekts': objekts,
                      'categories': MaterialCategory.objects.distinct('category').all()
                  })


@login_required
def objekt(request: HttpRequest, objekt_pk: int) -> HttpResponse:
    objekt = get_object_or_404(Objekt, pk=objekt_pk)

    if request.method == 'POST':
        objekt_form = ObjektForm(request.POST, request.FILES, instance=objekt)
        if objekt_form.is_valid():
            objekt_form.save()

            objekt.material.clear()
            categories = request.POST.getlist('subcategory[]')
            for category in categories:
                if category != '':
                    objekt.material.add(MaterialCategory.objects.get(pk=int(category)))

            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ContentType.objects.get_for_model(objekt).pk,
                object_id=objekt_pk,
                object_repr=str(objekt),
                change_message="Material wurde geändert",
                action_flag=CHANGE)
    else:
        objekt_form = ObjektForm(instance=objekt)

    return render(request=request,
                  template_name='objekt/pages/objekt_admin.html',
                  context={
                      'objekt': objekt,
                      'objekt_form': objekt_form,
                      'log_entries': LogEntry.objects.filter(
                          content_type_id=ContentType.objects.get_for_model(Objekt).pk,
                          object_id=objekt.id
                      ),
                      'categories': MaterialCategory.objects.distinct('category').all()
                  })


@login_required
def offer(request: HttpRequest, offer_pk: int) -> HttpResponse:
    offer = get_object_or_404(Offer, pk=offer_pk)

    if request.method == 'POST':
        offer_status = OfferStatus.objects.get(id=request.POST['status'])
        offer.offer_status = offer_status
        offer.save()

        OfferStatusLog.objects.create(
            offer=offer,
            offer_status=offer.offer_status,
            created_by=request.user
        )

    return render(request=request,
                  template_name='objekt/pages/offer_admin.html',
                  context={
                      'offer': offer,
                      'offer_statuses': OfferStatus.objects.all(),
                      'status_logs': []
                  })


@login_required
def objekt_comment(request, objekt_pk: int) -> HttpResponseRedirect:
    if request.method == 'POST':
        objekt = Objekt.objects.get(pk=objekt_pk)

        comment = Comment.objects.create(
            objekt_id=objekt_pk,
            created_by=request.user,
            text=request.POST['text']
        )

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Bemerkung wurde hinzugefügt",
            action_flag=CHANGE)

        template = get_template('objekt/components/objekt_comment.html')
        html = template.render(request=request, context={
            'objekt': objekt,
            'comment': comment
        })

        return JsonResponse({
            'success': True,
            'html': html
        })


def objekt_images(request, objekt_pk: int) -> HttpResponseRedirect:
    objekt = get_object_or_404(Objekt, pk=objekt_pk)

    files = request.FILES.getlist('file')

    for file_obj in files:
        # organize a path for the file in bucket
        file_directory_within_bucket = 'images/objekt/{objekt_id}/{guid}'.format(
            objekt_id=objekt.id,
            guid=str(uuid.uuid4())
        )

        # synthesize a full file path; note that we included the filename
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )

        media_storage = S3Boto3Storage()

        # avoid overwriting existing file
        if not media_storage.exists(file_path_within_bucket):
            media_storage.save(file_path_within_bucket, file_obj)

            file_url = "https://{}.s3.amazonaws.com/{}".format(
                'tuberlin-dev',
                file_path_within_bucket
            )

            image = Image.objects.create(filename=file_url)
            objekt.images.add(image)

            if objekt.thumbnail_image is None:
                objekt.thumbnail_image = image

            objekt.save()

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Material hatte neue Bilder hinzugefügt",
        action_flag=CHANGE)

    template = get_template('objekt/components/image_list.html')
    html = template.render(request=request, context={
        'objekt': objekt
    })

    return JsonResponse({
        'success': True,
        'html': html
    })


@login_required
def objekt_delete(request: HttpRequest, objekt_pk: int):
    objekt = get_object_or_404(Objekt, pk=objekt_pk)
    objekt.deleted_at = now()
    objekt.save()

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Material wurde gelöscht",
        action_flag=CHANGE)

    template = get_template('objekt/components/image_list.html')
    html = template.render(request=request, context={
        'objekt': objekt
    })

    return HttpResponseRedirect(redirect_to=reverse('inventory_objekt', args=(objekt_pk,)))


@login_required
def objekt_delete_forever_all(request: HttpRequest):
    objekts = Objekt.deleted_objects.all()

    for objekt in objekts:
        objekt.delete()

    return JsonResponse({
        'success': True
    })


@login_required
def objekt_undelete(request: HttpRequest, objekt_pk: int):
    objekt = get_object_or_404(Objekt, pk=objekt_pk)
    objekt.deleted_at = None
    objekt.save()

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Materiallöschung wurde rückgängig gemacht",
        action_flag=CHANGE)

    return HttpResponseRedirect(redirect_to=request.META['HTTP_REFERER'])


@login_required
def objekt_archive(request: HttpRequest, objekt_pk: int):
    objekt = get_object_or_404(Objekt, pk=objekt_pk)
    objekt.archived_at = now()
    objekt.save()

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Material wurde archiviert",
        action_flag=CHANGE)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def objekt_unarchive(request: HttpRequest, objekt_pk: int):
    objekt = get_object_or_404(Objekt, pk=objekt_pk)
    objekt.archived_at = None
    objekt.save()

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Material wurde ausarchiviert",
        action_flag=CHANGE)

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def objekt_comment_delete(request: HttpRequest, objekt_pk: int, comment_pk: int) -> HttpResponseRedirect:
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.objekt_id == objekt_pk:
        comment.deleted_at = now()
        comment.save()

    objekt = get_object_or_404(Objekt, pk=objekt_pk)

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Bemerkung wurde gelöscht",
        action_flag=CHANGE)

    return HttpResponseRedirect(redirect_to=reverse('inventory_objekt', args=(objekt_pk,)))


@login_required
def objekt_clone(request: HttpRequest) -> HttpResponseRedirect:
    objekt = Objekt.objects.get(pk=request.POST['objekt'])

    cloned_objekt = Objekt.objects.create(
        title=objekt.title + " (Klone)",
        count=objekt.count,
        unit=objekt.unit,
        width=objekt.width,
        length=objekt.length,
        height=objekt.height,
        depth=objekt.depth,
        condition=objekt.condition,
        mass=objekt.mass,
        treatment_notes=objekt.treatment_notes,
        description=objekt.description,
        price=objekt.price,
        cloned_from=objekt,
        offer=objekt.offer,
        reference_price=objekt.reference_price,
        eco_cost=objekt.eco_cost,
        created_by=request.user
    )

    for material in objekt.material.all():
        cloned_objekt.material.add(material)

    for image in objekt.images.all():
        cloned_objekt.images.add(image)

    cloned_objekt.thumbnail_image = objekt.thumbnail_image
    cloned_objekt.save()

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt.pk,
        object_repr=str(objekt),
        change_message="Material wurde geklont",
        action_flag=CHANGE)

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(cloned_objekt).pk,
        object_id=cloned_objekt.pk,
        object_repr=str(cloned_objekt),
        change_message="Material wurde erstellt",
        action_flag=ADDITION)

    return JsonResponse({
        'success': True, 'redirect_url': reverse('inventory_objekt', args=(cloned_objekt.id,))
    })


@login_required
def objekt_knowledge_base(request: HttpRequest, objekt_pk: int) -> HttpResponseRedirect:
    objekt = Objekt.objects.get(pk=objekt_pk)

    if 'knowledge_base' in request.POST:
        objekt.knowledge_base = True

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Material wurde zur KnowledgeBase hinzugefügt",
            action_flag=CHANGE)

    else:
        objekt.knowledge_base = False

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Material wurde aus der KnowledgeBase entfernt",
            action_flag=CHANGE)

    objekt.save()

    return JsonResponse({
        'success': True
    })


@login_required
def objekt_restado(request: HttpRequest, objekt_pk: int) -> HttpResponseRedirect:
    objekt = Objekt.objects.get(pk=objekt_pk)

    if 'restado' in request.POST:
        objekt.available_on_restado = True

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Material wurde für Restado zur Verfügung gestellt",
            action_flag=CHANGE)
    else:
        objekt.available_on_restado = False

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Materialverfügbarkeit auf Restado wurde entfernt",
            action_flag=CHANGE)

    objekt.save()

    return JsonResponse({
        'success': True
    })


@login_required
def objekt_sold_undo(request: HttpRequest, objekt_pk: int) -> HttpResponseRedirect:
    objekt = Objekt.objects.get(pk=objekt_pk)
    if objekt.partial_sale_parent:
        objekt.partial_sale_parent.count += objekt.sold_count
        objekt.partial_sale_parent.save()

        objekt.delete()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt.partial_sale_parent.id,
            object_repr=str(objekt.partial_sale_parent),
            change_message="Der Materialverkauf wurde rückgängig gemacht",
            action_flag=CHANGE)

        return JsonResponse({
            'success': True,
            'url': '/objekt/{}/'.format(objekt.partial_sale_parent.id)
        })

    else:
        objekt.count = objekt.sold_count
        objekt.sold_count = None
        objekt.sold_at = None
        objekt.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Der Materialverkauf wurde rückgängig gemacht",
            action_flag=CHANGE)

        objekt.refresh_from_db()
        template = get_template('objekt/components/sold.html')
        html = template.render(request=request, context={
            'objekt': objekt
        })

        return JsonResponse({
            'success': True,
            'html': html,
            'remaining_count': objekt.count
        })



@login_required
def objekt_sold(request: HttpRequest, objekt_pk: int) -> HttpResponseRedirect:
    objekt = Objekt.objects.get(pk=objekt_pk)

    sold_count = convert_float(request.POST['count'])
    price = convert_float(request.POST['price'])

    objekt.sell(sold_count, price, sold_by=request.user)

    LogEntry.objects.log_action(
        user_id=request.user.id,
        content_type_id=ContentType.objects.get_for_model(objekt).pk,
        object_id=objekt_pk,
        object_repr=str(objekt),
        change_message="Material wurde verkauft",
        action_flag=CHANGE)

    objekt.refresh_from_db()
    template = get_template('objekt/components/sold.html')
    html = template.render(request=request, context={
        'objekt': objekt
    })

    return JsonResponse({
        'success': True,
        'html': html,
        'remaining_count': objekt.count if objekt.count else ''
    })


@login_required
def objekt_aktions(request, objekt_pk):
    objekt = Objekt.objects.get(pk=objekt_pk)
    template = get_template('objekt/components/aktions.html')

    html = template.render(request=request, context={
        'objekt': objekt,
        'log_entries': LogEntry.objects.filter(
            content_type_id=ContentType.objects.get_for_model(Objekt).pk,
            object_id=objekt.id
        )
    })

    return JsonResponse({
        'success': True,
        'html': html
    })


@login_required
def objekt_images_delete(request, objekt_pk, image_pk):
    try:
        objekt = Objekt.objects.get(pk=objekt_pk)
    except objekt.DoesNotExist:
        objekt = None

    try:
        image = Image.objects.get(pk=image_pk)
    except image.DoesNotExist:
        image = None

    if objekt and image:
        objekt.images.remove(image)

        if objekt.thumbnail_image == image:
            objekt.thumbnail_image = objekt.images.first()

        objekt.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Bild wurde entfernt",
            action_flag=CHANGE)

    template = get_template('objekt/components/image_list.html')
    html = template.render(request=request, context={
        'objekt': objekt
    })

    return JsonResponse({
        'success': True,
        'html': html
    })


@login_required
def objekt_images_thumbnail(request, objekt_pk, image_pk):
    try:
        objekt = Objekt.objects.get(pk=objekt_pk)
    except objekt.DoesNotExist:
        objekt = None

    try:
        image = Image.objects.get(pk=image_pk)
    except image.DoesNotExist:
        image = None

    if objekt and image:
        objekt.thumbnail_image = image
        objekt.save()

        LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(objekt).pk,
            object_id=objekt_pk,
            object_repr=str(objekt),
            change_message="Ein anderes Hauptbild wurde gewählt",
            action_flag=CHANGE)

    template = get_template('objekt/components/image_list.html')
    html = template.render(request=request, context={
        'objekt': objekt
    })

    return JsonResponse({
        'success': True,
        'html': html
    })


@login_required
def person(request: HttpRequest, person_pk: int) -> HttpResponse:
    person = get_object_or_404(Person, pk=person_pk)

    if request.method == 'POST':
        person_form = PersonForm(request.POST, request.FILES, instance=person)
        if person_form.is_valid():
            person_form.save()
    else:
        person_form = PersonForm(instance=person)

    template_name = 'person/person.html'

    return render(request=request,
                  template_name=template_name,
                  context={
                      'person_form': person_form,
                      'person': person
                  })


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(redirect_to=reverse('inventory_objekt_dashboard_materials'))
    else:
        return HttpResponseRedirect(redirect_to='/offer/')


def material_autocomplete(request):
    value = request.GET['query'].strip()

    if value != '':
        suggestions = MaterialCategory.objects.filter(
            models.Q(text__icontains=value) | models.Q(category__icontains=value)
        )
    else:
        suggestions = MaterialCategory.objects.all()

    return JsonResponse({
        'success': True,
        'suggestions': [str(s) for s in suggestions]
    })


def subcategories_autocomplete(request):
    value = request.GET['category'].strip()

    subcategories = MaterialCategory.objects.filter(
        category=value
    ).order_by('subcategory').values('id', 'subcategory')

    for subc in subcategories:
        if not subc['subcategory']:
            subc['subcategory'] = '[nicht spezifiziert]'

    return JsonResponse({
        'success': True,
        'subcategories': list(subcategories)
    })


@login_required
def inventory_report(request):
    name = "gmit_inventory_bericht_{}.csv".format(datetime.datetime.now()).replace(" ", "_")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name)

    writer = csv.writer(response, dialect='excel')
    writer.writerow(["Haupttitel", "Materialkategorie", "Letzte Aktualisierung", "Hergestellt in",
                     "Einheit", "Länge (cm)", "Breite (cm)",
                     "Höhe (cm)", "Tiefe (cm)", "Gewicht (kg)",
                     "Einheitanzahl", "Beschreibung", "Zustand",
                     "Verkaufspreis", "Referenzpreis", "EcoCost", "Verkauft am",
                     "Verkaufte Einheit", "Verkaufspreis pro Einheit",
                     "Verkaufte Einheit * Verkaufspreis pro Einheit",
                     "Verkaufte Einheit * EcoCost"])

    for objekt in Objekt.objects.filter(deleted_at__isnull=True).order_by('sold_at', 'created_at').all():
        row = []

        row.append(objekt.title)
        row.append(" | ".join([str(m) for m in objekt.material.all()]))
        row.append(objekt.created_at)
        row.append(objekt.updated_at)
        row.append(objekt.unit)
        row.append(objekt.length)
        row.append(objekt.width)
        row.append(objekt.height)
        row.append(objekt.depth)
        row.append(objekt.mass)
        row.append(str(objekt.count).replace(".", ","))
        row.append(objekt.description)
        row.append(objekt.condition)
        row.append(objekt.price)
        row.append(objekt.reference_price)
        row.append(objekt.eco_cost)
        row.append(objekt.sold_at)
        row.append(str(objekt.sold_count).replace(".", ","))
        row.append(str(objekt.sold_price_per_unit).replace(".", ","))

        sold_price_per_unit = objekt.sold_price_per_unit * objekt.sold_count if (objekt.sold_price_per_unit and objekt.sold_count) else ''
        row.append(str(sold_price_per_unit).replace(".", ","))

        eco_cost = objekt.eco_cost * objekt.sold_count if (objekt.eco_cost and objekt.sold_count) else ''
        row.append(str(eco_cost).replace(".", ","))

        writer.writerow(row)

    return response


@login_required
def monthly_report(request):
    name = "gmit_monatlich_bericht_{}.csv".format(datetime.datetime.now()).replace(" ", "_")
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(name)

    writer = csv.writer(response)
    writer.writerow(["Zeitraum", "Insgesamt Verkaufspreis", "Insgesamt EcoCost", "Insgesamt"])

    objekts = Objekt.objects.filter(sold_at__isnull=False).annotate(zeitraum=TruncMonth('sold_at'))

    months = {}
    for objekt in objekts:
        if objekt.zeitraum not in months:
            months[objekt.zeitraum] = {
                'verkaufspreis': 0,
                'eco_cost': 0,
                'total_sales': 0
            }

        if objekt.sold_count and objekt.sold_price_per_unit:
            months[objekt.zeitraum]['verkaufspreis'] += objekt.sold_count * objekt.sold_price_per_unit

        if objekt.sold_count and objekt.eco_cost:
            months[objekt.zeitraum]['eco_cost'] += objekt.sold_count * objekt.eco_cost

        months[objekt.zeitraum]['total_sales'] += 1

    for key in sorted(list(months.keys())):
        value = months[key]
        writer.writerow([key, value['verkaufspreis'], value['eco_cost'], value['total_sales']])
    return response
