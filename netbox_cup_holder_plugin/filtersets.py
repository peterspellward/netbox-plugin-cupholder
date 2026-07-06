"""
Filtersets for NetBox Cup Holder Plugin.

For more information on NetBox filtersets, see:
https://docs.netbox.dev/en/stable/plugins/development/filtersets/

For django-filters documentation, see:
https://django-filter.readthedocs.io/
"""

import django_filters
from dcim.models import Rack, Site
from django.db.models import Q
from django.utils.translation import gettext as _
from netbox.filtersets import NetBoxModelFilterSet, PrimaryModelFilterSet

from .choices import CupholderMountFaceChoices, CupholderSizeChoices
from .models import Cupholder, CupholderType


class CupholderTypeFilterSet(PrimaryModelFilterSet):
    size = django_filters.MultipleChoiceFilter(
        choices=CupholderSizeChoices,
        label=_('Size'),
    )
    material = django_filters.CharFilter(
        lookup_expr='icontains',
        label=_('Material'),
    )

    class Meta:
        model = CupholderType
        fields = ('id', 'name', 'size', 'material')

    def search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
            | Q(material__icontains=value)
            | Q(description__icontains=value)
        )


class CupholderFilterSet(NetBoxModelFilterSet):
    cupholder_type_id = django_filters.ModelMultipleChoiceFilter(
        queryset=CupholderType.objects.all(),
        distinct=False,
        label=_('Cup holder type (ID)'),
    )
    size = django_filters.MultipleChoiceFilter(
        field_name='cupholder_type__size',
        choices=CupholderSizeChoices,
        label=_('Size'),
    )
    material = django_filters.CharFilter(
        field_name='cupholder_type__material',
        lookup_expr='icontains',
        label=_('Material'),
    )
    rack_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Rack.objects.all(),
        distinct=False,
        label=_('Rack (ID)'),
    )
    rack = django_filters.ModelMultipleChoiceFilter(
        field_name='rack__name',
        queryset=Rack.objects.all(),
        distinct=False,
        to_field_name='name',
        label=_('Rack (name)'),
    )
    mount_face = django_filters.MultipleChoiceFilter(
        choices=CupholderMountFaceChoices,
        label=_('Mount face'),
    )
    site_id = django_filters.ModelMultipleChoiceFilter(
        field_name='rack__site',
        queryset=Site.objects.all(),
        distinct=False,
        label=_('Site (ID)'),
    )
    site = django_filters.ModelMultipleChoiceFilter(
        field_name='rack__site__slug',
        queryset=Site.objects.all(),
        distinct=False,
        to_field_name='slug',
        label=_('Site (slug)'),
    )

    class Meta:
        model = Cupholder
        fields = (
            'id',
            'name',
            'cupholder_type_id',
            'size',
            'material',
            'rack_id',
            'rack',
            'mount_face',
            'site_id',
            'site',
        )

    def search(self, queryset, name, value):
        return queryset.filter(name__icontains=value)
