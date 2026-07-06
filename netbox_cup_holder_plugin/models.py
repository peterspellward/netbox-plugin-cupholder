"""
Models for NetBox Cup Holder Plugin.

For more information on NetBox models, see:
https://docs.netbox.dev/en/stable/plugins/development/models/

For NetBox model features (tags, custom fields, change logging, etc.), see:
https://docs.netbox.dev/en/stable/development/models/#netbox-model-features
"""

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from netbox.models import NetBoxModel, PrimaryModel

from .choices import CupholderMountFaceChoices, CupholderSizeChoices


class CupholderType(PrimaryModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    size = models.CharField(
        max_length=10,
        choices=CupholderSizeChoices,
    )
    material = models.CharField(
        max_length=100,
    )

    class Meta:
        app_label = "netbox_cup_holder_plugin"
        ordering = ("name",)
        verbose_name = _('cup holder type')
        verbose_name_plural = _('cup holder types')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("plugins:netbox_cup_holder_plugin:cupholdertype", args=[self.pk])


class Cupholder(NetBoxModel):
    name = models.CharField(max_length=100, unique=True)
    cupholder_type = models.ForeignKey(
        to='CupholderType',
        on_delete=models.PROTECT,
        related_name='cupholders',
    )
    rack = models.OneToOneField(
        to='dcim.Rack',
        on_delete=models.PROTECT,
        related_name='cupholder',
    )
    mount_face = models.CharField(
        max_length=50,
        choices=CupholderMountFaceChoices,
        verbose_name=_('Mount face'),
    )

    class Meta:
        app_label = "netbox_cup_holder_plugin"
        ordering = ("rack", "name")
        verbose_name_plural = "Cupholders"

    def __str__(self):
        return f'{self.name} ({self.cupholder_type}, {self.rack})'

    def get_absolute_url(self):
        return reverse("plugins:netbox_cup_holder_plugin:cupholder", args=[self.pk])

    def clean(self):
        super().clean()

        if self.mount_face and self.mount_face not in CupholderMountFaceChoices.values():
            raise ValidationError({
                'mount_face': _('Select a valid mount face. Valid choices are: front, left, right.'),
            })

        if self.rack_id:
            duplicate_qs = Cupholder.objects.filter(rack_id=self.rack_id)
            if self.pk:
                duplicate_qs = duplicate_qs.exclude(pk=self.pk)
            if duplicate_qs.exists():
                raise ValidationError({
                    'rack': _('This rack already has a cup holder assigned.'),
                })
