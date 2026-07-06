"""
API serializers for NetBox Cup Holder Plugin.

Serializers are required for NetBox event handling (webhooks, change logging).
They also power the REST API endpoints.

For more information on NetBox REST API serializers, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#serializers

For Django REST Framework serializers, see:
https://www.django-rest-framework.org/api-guide/serializers/
"""

from dcim.api.serializers import RackSerializer
from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from rest_framework import serializers

from ..choices import CupholderMountFaceChoices, CupholderSizeChoices
from ..models import Cupholder, CupholderType


class CupholderTypeSerializer(PrimaryModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_cup_holder_plugin-api:cupholdertype-detail'
    )
    size = ChoiceField(choices=CupholderSizeChoices)

    class Meta:
        model = CupholderType
        fields = (
            'id',
            'url',
            'display',
            'name',
            'size',
            'material',
            'description',
            'comments',
            'tags',
            'custom_fields',
            'created',
            'last_updated',
        )


class CupholderSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_cup_holder_plugin-api:cupholder-detail"
    )
    cupholder_type = CupholderTypeSerializer(nested=True)
    rack = RackSerializer(nested=True)
    mount_face = ChoiceField(choices=CupholderMountFaceChoices)

    class Meta:
        model = Cupholder
        fields = (
            "id",
            "url",
            "display",
            "name",
            "cupholder_type",
            "rack",
            "mount_face",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )
