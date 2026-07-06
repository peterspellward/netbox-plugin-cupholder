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
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from netbox.api.fields import ChoiceField
from netbox.api.serializers import NetBoxModelSerializer, PrimaryModelSerializer
from rest_framework import serializers

from ..choices import CupholderMountFaceChoices, CupholderSizeChoices
from ..models import Cupholder, CupholderType


def _django_validation_error_to_drf(exc: DjangoValidationError) -> serializers.ValidationError:
    if hasattr(exc, 'message_dict') and exc.message_dict:
        return serializers.ValidationError(exc.message_dict)
    if hasattr(exc, 'messages'):
        return serializers.ValidationError(exc.messages)
    return serializers.ValidationError(str(exc))


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
        brief_fields = ('id', 'url', 'display', 'name', 'size', 'material', 'description')


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
        brief_fields = ('id', 'url', 'display', 'name', 'mount_face')

    def validate(self, data):
        try:
            return super().validate(data)
        except DjangoValidationError as exc:
            raise _django_validation_error_to_drf(exc) from exc

    def validate_rack(self, rack):
        duplicate_qs = Cupholder.objects.filter(rack=rack)
        if self.instance:
            duplicate_qs = duplicate_qs.exclude(pk=self.instance.pk)
        if duplicate_qs.exists():
            raise serializers.ValidationError(_('This rack already has a cup holder assigned.'))
        return rack
