"""
Views for NetBox Cup Holder Plugin.

For more information on NetBox views, see:
https://docs.netbox.dev/en/stable/plugins/development/views/

For generic view classes, see:
https://docs.netbox.dev/en/stable/development/views/
"""

from netbox.views import generic

from . import filtersets, forms, models, tables


class CupholderTypeView(generic.ObjectView):
    queryset = models.CupholderType.objects.all()
    template_name = 'netbox_cup_holder_plugin/cupholdertype.html'


class CupholderTypeListView(generic.ObjectListView):
    queryset = models.CupholderType.objects.all()
    table = tables.CupholderTypeTable
    filterset = filtersets.CupholderTypeFilterSet


class CupholderTypeEditView(generic.ObjectEditView):
    queryset = models.CupholderType.objects.all()
    form = forms.CupholderTypeForm


class CupholderTypeDeleteView(generic.ObjectDeleteView):
    queryset = models.CupholderType.objects.all()


class CupholderView(generic.ObjectView):
    queryset = models.Cupholder.objects.all()
    template_name = 'netbox_cup_holder_plugin/cupholder.html'


class CupholderListView(generic.ObjectListView):
    queryset = models.Cupholder.objects.all()
    table = tables.CupholderTable
    filterset = filtersets.CupholderFilterSet


class CupholderEditView(generic.ObjectEditView):
    queryset = models.Cupholder.objects.all()
    form = forms.CupholderForm


class CupholderDeleteView(generic.ObjectDeleteView):
    queryset = models.Cupholder.objects.all()
