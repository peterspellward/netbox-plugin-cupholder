"""
Template extensions for NetBox Cup Holder Plugin.
"""

from netbox.plugins import PluginTemplateExtension


class RackCupholder(PluginTemplateExtension):
    models = ['dcim.rack']

    def full_width_page(self):
        rack = self.context['object']
        cupholder = getattr(rack, 'cupholder', None)
        return self.render('netbox_cup_holder_plugin/inc/rack_cupholders.html', extra_context={
            'cupholder': cupholder,
        })


template_extensions = [
    RackCupholder,
]
