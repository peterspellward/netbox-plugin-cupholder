"""
Search indexes for NetBox Cup Holder Plugin.

This module defines search indexes to make plugin models searchable in NetBox's
global search. See: https://docs.netbox.dev/en/stable/plugins/development/search/
"""

from netbox.search import SearchIndex

from .models import Cupholder, CupholderType


class CupholderTypeIndex(SearchIndex):
    """Search index for CupholderType catalog entries."""

    model = CupholderType

    fields = (
        ('name', 100),
        ('material', 200),
        ('description', 500),
    )

    display_attrs = (
        'size',
        'material',
    )


class CupholderIndex(SearchIndex):
    """Search index for Cupholder instances."""

    model = Cupholder

    fields = (
        ('name', 100),
    )

    display_attrs = (
        'cupholder_type',
        'rack',
        'mount_face',
    )


indexes = (
    CupholderTypeIndex,
    CupholderIndex,
)
