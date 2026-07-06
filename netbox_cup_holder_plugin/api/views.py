"""
API viewsets for NetBox Cup Holder Plugin.

For more information on NetBox REST API viewsets, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#viewsets

For Django REST Framework viewsets, see:
https://www.django-rest-framework.org/api-guide/viewsets/
"""

from netbox.api.viewsets import NetBoxModelViewSet

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
