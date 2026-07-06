"""
API viewsets for NetBox Cup Holder Plugin.

For more information on NetBox REST API viewsets, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#viewsets

For Django REST Framework viewsets, see:
https://www.django-rest-framework.org/api-guide/viewsets/
"""

from django.db import IntegrityError
from django.utils.translation import gettext_lazy as _
from netbox.api.viewsets import NetBoxModelViewSet
from rest_framework.exceptions import ValidationError

from .. import filtersets
from ..models import Cupholder, CupholderType
from .serializers import CupholderSerializer, CupholderTypeSerializer


class CupholderTypeViewSet(NetBoxModelViewSet):
    queryset = CupholderType.objects.all()
    serializer_class = CupholderTypeSerializer
    filterset_class = filtersets.CupholderTypeFilterSet


class CupholderViewSet(NetBoxModelViewSet):
    queryset = Cupholder.objects.all()
    serializer_class = CupholderSerializer
    filterset_class = filtersets.CupholderFilterSet

    def perform_create(self, serializer):
        try:
            super().perform_create(serializer)
        except IntegrityError as exc:
            raise ValidationError({
                'non_field_errors': [_('Duplicate or invalid data.')],
            }) from exc
