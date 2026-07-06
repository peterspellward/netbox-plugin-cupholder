"""
URL patterns for NetBox Cup Holder Plugin.

For more information on URL routing, see:
https://docs.netbox.dev/en/stable/plugins/development/views/#url-registration

For Django URL patterns, see:
https://docs.djangoproject.com/en/stable/topics/http/urls/
"""

from django.urls import path
from netbox.views.generic import ObjectChangeLogView

from . import models, views

urlpatterns = (
    path("cup-holder-types/", views.CupholderTypeListView.as_view(), name="cupholdertype_list"),
    path("cup-holder-types/add/", views.CupholderTypeEditView.as_view(), name="cupholdertype_add"),
    path("cup-holder-types/<int:pk>/", views.CupholderTypeView.as_view(), name="cupholdertype"),
    path("cup-holder-types/<int:pk>/edit/", views.CupholderTypeEditView.as_view(), name="cupholdertype_edit"),
    path("cup-holder-types/<int:pk>/delete/", views.CupholderTypeDeleteView.as_view(), name="cupholdertype_delete"),
    path(
        "cup-holder-types/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="cupholdertype_changelog",
        kwargs={"model": models.CupholderType},
    ),
    path("cup-holders/", views.CupholderListView.as_view(), name="cupholder_list"),
    path("cup-holders/add/", views.CupholderEditView.as_view(), name="cupholder_add"),
    path("cup-holders/<int:pk>/", views.CupholderView.as_view(), name="cupholder"),
    path("cup-holders/<int:pk>/edit/", views.CupholderEditView.as_view(), name="cupholder_edit"),
    path("cup-holders/<int:pk>/delete/", views.CupholderDeleteView.as_view(), name="cupholder_delete"),
    path(
        "cup-holders/<int:pk>/changelog/",
        ObjectChangeLogView.as_view(),
        name="cupholder_changelog",
        kwargs={"model": models.Cupholder},
    ),
)
