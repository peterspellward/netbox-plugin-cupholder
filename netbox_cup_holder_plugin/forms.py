"""
Forms for NetBox Cup Holder Plugin.

For more information on NetBox forms, see:
https://docs.netbox.dev/en/stable/plugins/development/forms/
"""

from dcim.models import Rack
from django import forms
from netbox.forms import NetBoxModelForm, PrimaryModelForm
from utilities.forms.fields import DynamicModelChoiceField
from utilities.forms.rendering import FieldSet

from .choices import CupholderMountFaceChoices, CupholderSizeChoices
from .models import Cupholder, CupholderType


class CupholderTypeForm(PrimaryModelForm):
    size = forms.ChoiceField(
        choices=CupholderSizeChoices,
    )

    fieldsets = (
        FieldSet('name', 'size', 'material', 'description', 'tags', name='Cup Holder Type'),
    )

    class Meta:
        model = CupholderType
        fields = ('name', 'size', 'material', 'description', 'comments', 'tags')


class CupholderForm(NetBoxModelForm):
    cupholder_type = DynamicModelChoiceField(
        queryset=CupholderType.objects.all(),
    )
    rack = DynamicModelChoiceField(
        queryset=Rack.objects.all(),
        selector=True,
    )
    mount_face = forms.ChoiceField(
        choices=CupholderMountFaceChoices,
    )

    fieldsets = (
        FieldSet('name', 'cupholder_type', 'tags', name='Cup Holder'),
        FieldSet('rack', 'mount_face', name='Rack Mount'),
    )

    class Meta:
        model = Cupholder
        fields = ("name", "cupholder_type", "rack", "mount_face", "tags")
