"""
GraphQL schema for NetBox Cup Holder Plugin.

For more information on NetBox GraphQL, see:
https://docs.netbox.dev/en/stable/plugins/development/graphql/

For Strawberry GraphQL documentation, see:
https://strawberry.rocks/
"""

from typing import TYPE_CHECKING, Annotated

import strawberry
import strawberry_django

from . import models

if TYPE_CHECKING:
    from dcim.graphql.types import RackType


@strawberry_django.type(
    models.CupholderType,
    fields='__all__',
)
class CupholderType:
    """GraphQL type for CupholderType catalog entries."""


@strawberry_django.type(
    models.Cupholder,
    fields='__all__',
)
class Cupholder:
    """GraphQL type for Cupholder instances."""

    rack: Annotated['RackType', strawberry.lazy('dcim.graphql.types')]
    cupholder_type: Annotated['CupholderType', strawberry.lazy('netbox_cup_holder_plugin.graphql')]


@strawberry.type(name="Query")
class CupholderQuery:
    """GraphQL queries for NetBox Cup Holder Plugin."""

    cupholder: Cupholder = strawberry_django.field()
    cupholder_list: list[Cupholder] = strawberry_django.field()
    cupholder_type: CupholderType = strawberry_django.field()
    cupholder_type_list: list[CupholderType] = strawberry_django.field()


schema = [
    CupholderQuery,
]
