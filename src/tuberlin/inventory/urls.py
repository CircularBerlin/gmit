from django.urls import path
from rest_framework import routers
from django.conf.urls import url, include
import inventory.views as views

person_router = routers.DefaultRouter()
person_router.register(r'person', views.PersonAPIViewSet)

all_offers_router = routers.DefaultRouter()
all_offers_router.register(r'offers/all', views.OfferAllAPIViewSet)

pending_router = routers.DefaultRouter()
pending_router.register(r'offers/pending', views.OfferPendingAPIViewSet)

accepted_router = routers.DefaultRouter()
accepted_router.register(r'offers/accepted', views.OfferAcceptedAPIViewSet)

rejected_router = routers.DefaultRouter()
rejected_router.register(r'offers/rejected', views.OfferRejectedAPIViewSet)

all_objekts_router = routers.DefaultRouter()
all_objekts_router.register(r'objekts/all', views.ObjektAllAPIViewSet)

warehouse_router = routers.DefaultRouter()
warehouse_router.register(r'objekts/warehouse', views.ObjektWarehouseAPIViewSet)

available_router = routers.DefaultRouter()
available_router.register(r'objekts/available', views.ObjektAvailableAPIViewSet)

sold_router = routers.DefaultRouter()
sold_router.register(r'objekts/sold', views.ObjektSoldAPIViewSet)

archived_router = routers.DefaultRouter()
archived_router.register(r'objekts/archived', views.ObjektArchivedAPIViewSet)

deleted_router = routers.DefaultRouter()
deleted_router.register(r'objekts/deleted', views.ObjektDeletedAPIViewSet)

restado_router = routers.DefaultRouter()
restado_router.register(r'inventory', views.RestadoObjektAPIViewSet)
restado_router.register(r'material', views.RestadoMaterialAPIViewSet)


urlpatterns = [
    # *************************************************************************
    #
    # API routing
    #
    # *************************************************************************

    url('^api/', include(all_offers_router.urls)),
    url('^api/', include(pending_router.urls)),
    url('^api/', include(accepted_router.urls)),
    url('^api/', include(rejected_router.urls)),

    url('^api/', include(all_objekts_router.urls)),
    url('^api/', include(warehouse_router.urls)),
    url('^api/', include(available_router.urls)),
    url('^api/', include(sold_router.urls)),
    url('^api/', include(archived_router.urls)),
    url('^api/', include(deleted_router.urls)),

    url('^api/', include(person_router.urls)),

    url('^restado/api/', include(restado_router.urls)),

    # *************************************************************************
    #
    # objekt views and endpoints
    #
    # *************************************************************************

    path('objekt/<int:objekt_pk>/comment/<int:comment_pk>/delete/',
         views.objekt_comment_delete,
         name='inventory_objekt_comment_delete'),

    path('objekt/<int:objekt_pk>/comment/',
         views.objekt_comment,
         name='inventory_objekt_comment'),

    path('objekt/delete/forever/all/',
         views.objekt_delete_forever_all,
         name='inventory_objekt_delete_forever_all'),

    path('objekt/<int:objekt_pk>/delete/',
         views.objekt_delete,
         name='inventory_objekt_delete'),

    path('objekt/<int:objekt_pk>/undelete/',
         views.objekt_undelete,
         name='inventory_objekt_undelete'),

    path('objekt/<int:objekt_pk>/archive/',
         views.objekt_archive,
         name='inventory_objekt_archive'),

    path('objekt/<int:objekt_pk>/unarchive/',
         views.objekt_unarchive,
         name='inventory_objekt_unarchive'),

    path('objekt/<int:objekt_pk>/image/<int:image_pk>/delete/',
         views.objekt_images_delete,
         name='inventory_objekt_images_delete'),

    path('objekt/<int:objekt_pk>/image/<int:image_pk>/thumbnail/',
         views.objekt_images_thumbnail,
         name='inventory_objekt_images_thumbnail'),

    path('objekt/<int:objekt_pk>/images/',
         views.objekt_images,
         name='inventory_objekt_images'),

    path('objekt/clone/',
         views.objekt_clone,
         name='inventory_objekt_clone'),

    path('objekt/<int:objekt_pk>/',
         views.objekt,
         name='inventory_objekt'),

    path('offer/<int:offer_pk>/transform/',
         views.offer_transform,
         name='inventory_offer_transform'),

    path('objekt/<int:objekt_pk>/knowledgebase/',
         views.objekt_knowledge_base,
         name='inventory_objekt_knowledge_base'),

    path('objekt/<int:objekt_pk>/restado/',
         views.objekt_restado,
         name='inventory_objekt_restado'),

    path('objekt/<int:objekt_pk>/aktions/',
         views.objekt_aktions,
         name='inventory_objekt_aktions'),


    path('objekt/<int:objekt_pk>/sold/',
         views.objekt_sold,
         name='inventory_objekt_sold'),

    path('offer/<int:offer_pk>/delete/',
         views.offer_delete,
         name='inventory_offer_delete'),

    path('offer/<int:offer_pk>/',
         views.offer,
         name='inventory_offer'),

    path('offer/',
         views.offer_create,
         name='inventory_offer_create'),

    path('objekt/',
         views.objekt_create,
         name='inventory_objekt_create'),

    # *************************************************************************
    #
    # person
    #
    # *************************************************************************

    path('person/<int:person_pk>/',
         views.person,
         name='inventory_person'),


    # *************************************************************************
    #
    # dashboards
    #
    # *************************************************************************

    path('dashboard/people/',
         views.people_dashboard,
         name='inventory_people_dashboard'),

    path('dashboard/offers/',
         views.objekt_dashboard_offers,
         name='inventory_objekt_dashboard_offers'),

    path('dashboard/pending/',
         views.objekt_dashboard_pending,
         name='inventory_objekt_dashboard_pending'),

    path('dashboard/accepted/',
         views.objekt_dashboard_accepted,
         name='inventory_objekt_dashboard_accepted'),

    path('dashboard/rejected/',
         views.objekt_dashboard_rejected,
         name='inventory_objekt_dashboard_rejected'),

    path('dashboard/materials/',
         views.objekt_dashboard_materials,
         name='inventory_objekt_dashboard_materials'),

    path('dashboard/warehouse/',
         views.objekt_dashboard_warehouse,
         name='inventory_objekt_dashboard_warehouse'),

    path('dashboard/available/',
         views.objekt_dashboard_available,
         name='inventory_objekt_dashboard_available'),

    path('dashboard/sold/',
         views.objekt_dashboard_sold,
         name='inventory_objekt_dashboard_sold'),

    path('dashboard/archived/',
         views.objekt_dashboard_archived,
         name='inventory_objekt_dashboard_archived'),

    path('dashboard/deleted/',
         views.objekt_dashboard_deleted,
         name='inventory_objekt_dashboard_deleted'),

    path('report/inventory/', views.inventory_report, name='inventory_report'),
    path('report/monthly/', views.monthly_report, name='monthly_report'),

    # *************************************************************************
    #
    # index
    #
    # *************************************************************************

    path('', views.index, name='inventory_index'),

    # *************************************************************************
    #
    # accounts
    #
    # *************************************************************************

    path('accounts/', include('django.contrib.auth.urls')),

    path('autocomplete/material/', views.material_autocomplete)
]

