"""
API URL patterns for NetBox Cup Holder Plugin.

For more information on NetBox REST API routing, see:
https://docs.netbox.dev/en/stable/plugins/development/rest-api/#routers

For Django REST Framework routers, see:
https://www.django-rest-framework.org/api-guide/routers/
"""

from netbox.api.routers import NetBoxRouter

from .views import CupholderTypeViewSet, CupholderViewSet

app_name = "netbox_cup_holder_plugin"

router = NetBoxRouter()
router.register("cup-holder-types", CupholderTypeViewSet)
router.register("cup-holders", CupholderViewSet)

urlpatterns = router.urls
