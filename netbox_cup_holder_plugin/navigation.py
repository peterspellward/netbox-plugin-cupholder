"""
Navigation menu items for NetBox Cup Holder Plugin.

For more information on navigation menus, see:
https://docs.netbox.dev/en/stable/plugins/development/navigation/
"""

from netbox.plugins import PluginMenuButton, PluginMenuItem

cupholder_buttons = [
    PluginMenuButton(
        link="plugins:netbox_cup_holder_plugin:cupholder_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

cupholder_type_buttons = [
    PluginMenuButton(
        link="plugins:netbox_cup_holder_plugin:cupholdertype_add",
        title="Add",
        icon_class="mdi mdi-plus-thick",
    )
]

menu_items = (
    PluginMenuItem(
        link="plugins:netbox_cup_holder_plugin:cupholder_list",
        link_text="Cup Holders",
        buttons=cupholder_buttons,
    ),
    PluginMenuItem(
        link="plugins:netbox_cup_holder_plugin:cupholdertype_list",
        link_text="Cup Holder Types",
        buttons=cupholder_type_buttons,
    ),
)
