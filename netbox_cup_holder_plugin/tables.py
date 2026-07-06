"""
Tables for NetBox Cup Holder Plugin.

For more information on NetBox tables, see:
https://docs.netbox.dev/en/stable/plugins/development/tables/

For django-tables2 documentation, see:
https://django-tables2.readthedocs.io/
"""

import django_tables2 as tables
from netbox.tables import NetBoxTable, columns

from .models import Cupholder, CupholderType


class CupholderTypeTable(NetBoxTable):
    name = tables.Column(linkify=True)
    size = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = CupholderType
        fields = ('pk', 'id', 'name', 'size', 'material', 'actions')
        default_columns = ('name', 'size', 'material')


class CupholderTable(NetBoxTable):
    name = tables.Column(linkify=True)
    cupholder_type = tables.Column(linkify=True)
    rack = tables.Column(linkify=True)
    mount_face = columns.ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = Cupholder
        fields = ('pk', 'id', 'name', 'cupholder_type', 'rack', 'mount_face', 'actions')
        default_columns = ('name', 'cupholder_type', 'rack', 'mount_face')
