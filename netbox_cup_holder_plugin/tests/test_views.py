"""
Test cases for NetBox Cup Holder Plugin views.
"""

from django.urls import reverse

from ..choices import CupholderMountFaceChoices
from ..models import Cupholder, CupholderType
from ..testing import PluginViewTestCase
from ..testing.utils import create_cupholder, create_cupholder_type, create_rack, disable_warnings, get_random_string


class CupholderTypeViewTestCase(PluginViewTestCase):
    """Test CupholderType views."""

    def test_list_cupholder_types(self):
        """Test cup holder type list view."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholdertype')

        url = reverse('plugins:netbox_cup_holder_plugin:cupholdertype_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_view_cupholder_type(self):
        """Test cup holder type detail view."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholdertype')

        model = CupholderType.objects.get(name='The Contractor')
        url = reverse('plugins:netbox_cup_holder_plugin:cupholdertype', kwargs={'pk': model.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertContains(response, 'The Contractor')
        self.assertContains(response, 'Stainless Steel')


class CupholderViewTestCase(PluginViewTestCase):
    """Test Cupholder views."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        cls.cupholder_type = create_cupholder_type(name='View Type')
        cls.rack = create_rack(name='View Rack')
        create_cupholder(
            name='View Test 1',
            rack=cls.rack,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_FRONT,
        )

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.base_url = 'plugins:netbox_cup_holder_plugin:cupholder'

    def test_list_cupholders(self):
        """Test Cupholder list view."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_list')
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)

    def test_list_cupholders_without_permission(self):
        """Test Cupholder list view without permission."""
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_list')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_view_cupholder(self):
        """Test Cupholder detail view."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        instance = Cupholder.objects.first()
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder', kwargs={'pk': instance.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.context['object'], instance)

    def test_create_cupholder(self):
        """Test creating a Cupholder via form."""
        self.add_permissions(
            'netbox_cup_holder_plugin.add_cupholder',
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
            'dcim.view_rack',
        )

        rack = create_rack()
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_add')
        name = f'Created {get_random_string(10)}'

        form_data = self.post_data({
            'name': name,
            'cupholder_type': self.cupholder_type,
            'rack': rack,
            'mount_face': CupholderMountFaceChoices.FACE_RIGHT,
            'tags': [],
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        instance = Cupholder.objects.get(name=name)
        self.assertEqual(instance.name, name)
        self.assertEqual(instance.rack, rack)
        self.assertEqual(instance.cupholder_type, self.cupholder_type)
        self.assertEqual(instance.mount_face, CupholderMountFaceChoices.FACE_RIGHT)

    def test_create_cupholder_without_permission(self):
        """Test creating a Cupholder without permission."""
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_add')

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_edit_cupholder(self):
        """Test editing a Cupholder via form."""
        self.add_permissions(
            'netbox_cup_holder_plugin.change_cupholder',
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
            'dcim.view_rack',
        )

        instance = Cupholder.objects.first()
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_edit', kwargs={'pk': instance.pk})

        get_response = self.client.get(url)
        self.assertHttpStatus(get_response, 200)

        new_name = f'Edited {get_random_string(10)}'
        form_data = self.post_data({
            'name': new_name,
            'cupholder_type': instance.cupholder_type,
            'rack': instance.rack,
            'mount_face': CupholderMountFaceChoices.FACE_LEFT,
            'tags': list(instance.tags.values_list('pk', flat=True)),
            '_init_time': get_response.context['form']['_init_time'].value(),
        })

        response = self.client.post(url, form_data, follow=True)
        self.assertHttpStatus(response, 200)

        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)
        self.assertEqual(instance.mount_face, CupholderMountFaceChoices.FACE_LEFT)

    def test_delete_cupholder(self):
        """Test deleting a Cupholder."""
        self.add_permissions(
            'netbox_cup_holder_plugin.delete_cupholder',
            'netbox_cup_holder_plugin.view_cupholder'
        )

        instance = Cupholder.objects.first()
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_delete', kwargs={'pk': instance.pk})

        response = self.client.post(url, {'confirm': True}, follow=True)
        self.assertHttpStatus(response, 200)

        self.assertFalse(
            Cupholder.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_cupholder_without_permission(self):
        """Test deleting a Cupholder without permission."""
        instance = Cupholder.objects.first()
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_delete', kwargs={'pk': instance.pk})

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_rack_detail_shows_cupholder(self):
        """Test that the rack detail page shows the mounted cup holder."""
        self.add_permissions(
            'dcim.view_rack',
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
        )

        url = reverse('dcim:rack', kwargs={'pk': self.rack.pk})
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertContains(response, 'Cup Holder')
        self.assertContains(response, 'View Test 1')
        self.assertContains(response, 'View Type')


class CupholderFormTestCase(PluginViewTestCase):
    """Test Cupholder form validation."""

    @classmethod
    def setUpTestData(cls):
        cls.rack = create_rack()
        cls.cupholder_type = create_cupholder_type()

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions(
            'netbox_cup_holder_plugin.add_cupholder',
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
            'dcim.view_rack',
        )

    def test_form_validation_empty_name(self):
        """Test form validation with empty name."""
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_add')
        form_data = self.post_data({
            'name': '',
            'cupholder_type': self.cupholder_type,
            'rack': self.rack,
            'mount_face': CupholderMountFaceChoices.FACE_FRONT,
            'tags': [],
        })

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)

        self.assertEqual(Cupholder.objects.filter(name='').count(), 0)

    def test_form_validation_duplicate_name(self):
        """Test form validation with duplicate name."""
        create_cupholder(name='Duplicate', rack=create_rack(), cupholder_type=self.cupholder_type)

        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_add')
        form_data = self.post_data({
            'name': 'Duplicate',
            'cupholder_type': self.cupholder_type,
            'rack': self.rack,
            'mount_face': CupholderMountFaceChoices.FACE_FRONT,
            'tags': [],
        })

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)

        self.assertEqual(Cupholder.objects.filter(name='Duplicate').count(), 1)

    def test_form_validation_invalid_mount_face(self):
        """Test form validation rejects invalid mount faces such as rear."""
        url = reverse('plugins:netbox_cup_holder_plugin:cupholder_add')
        form_data = self.post_data({
            'name': 'Invalid Face',
            'cupholder_type': self.cupholder_type,
            'rack': self.rack,
            'mount_face': 'rear',
            'tags': [],
        })

        response = self.client.post(url, form_data)
        self.assertHttpStatus(response, 200)

        self.assertFalse(Cupholder.objects.filter(name='Invalid Face').exists())
