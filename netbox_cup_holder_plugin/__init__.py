"""
NetBox Cup Holder Plugin

Plugin configuration for NetBox Cup Holder Plugin.

For a complete list of PluginConfig attributes, see:
https://docs.netbox.dev/en/stable/plugins/development/#pluginconfig-attributes
"""

__author__ = """Peter Spellward"""
__email__ = ""
__version__ = "0.1.0"


from netbox.plugins import PluginConfig


class CupholderConfig(PluginConfig):
    name = "netbox_cup_holder_plugin"
    verbose_name = "NetBox Cup Holder Plugin"
    description = "Netbox plugin for Cup Holders"
    author= "Peter Spellward"
    author_email = ""
    version = __version__
    base_url = "netbox_cup_holder_plugin"
    min_version = "4.5.0"
    max_version = "4.6.99"
    graphql_schema = "graphql.schema"


config = CupholderConfig
