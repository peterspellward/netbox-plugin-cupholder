"""
Test cases for NetBox Cup Holder Plugin REST API.
"""
from ..choices import CupholderMountFaceChoices, CupholderSizeChoices
from ..models import Cupholder, CupholderType
from ..testing import PluginAPITestCase
from ..testing.utils import (
    create_cupholder,
    create_cupholder_type,
    create_rack,
    disable_warnings,
    get_random_string,
)


class CupholderTypeAPITestCase(PluginAPITestCase):
    """Test CupholderType API endpoints."""

    def setUp(self):
        super().setUp()
        self.list_url_name = 'plugins-api:netbox_cup_holder_plugin-api:cupholdertype-list'
        self.detail_url_name = 'plugins-api:netbox_cup_holder_plugin-api:cupholdertype-detail'

    def test_list_cupholder_types(self):
        """Test GET request to list cup holder types."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholdertype')

        response = self.client.get(self._get_list_url())
        self.assertHttpStatus(response, 200)
        self.assertGreaterEqual(response.data['count'], 12)

    def test_get_cupholder_type(self):
        """Test GET request for a single cup holder type."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholdertype')

        model = CupholderType.objects.get(name='Weekend Warrior')
        response = self.client.get(self._get_detail_url(model))

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['size']['value'], CupholderSizeChoices.SIZE_XXL)

    def test_filter_cupholder_types_by_size(self):
        """Test filtering cup holder types by size."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholdertype')

        response = self.client.get(self._get_list_url(), {'size': CupholderSizeChoices.SIZE_XS})
        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Italiano Decadence')


class CupholderAPITestCase(PluginAPITestCase):
    """Test Cupholder API endpoints."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        cls.cupholder_type = create_cupholder_type(name='API Type')
        cls.rack1 = create_rack(name='API Rack 1')
        cls.rack2 = create_rack(name='API Rack 2')
        cls.rack3 = create_rack(name='API Rack 3')
        create_cupholder(
            name='API Test 1',
            rack=cls.rack1,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_FRONT,
        )
        create_cupholder(
            name='API Test 2',
            rack=cls.rack2,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_LEFT,
        )
        create_cupholder(
            name='API Test 3',
            rack=cls.rack3,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_RIGHT,
        )

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.list_url_name = 'plugins-api:netbox_cup_holder_plugin-api:cupholder-list'
        self.detail_url_name = 'plugins-api:netbox_cup_holder_plugin-api:cupholder-detail'

    def test_list_cupholders(self):
        """Test GET request to list Cupholders."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        url = self._get_list_url()
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 3)
        self.assertIn('results', response.data)

    def test_list_cupholders_without_permission(self):
        """Test GET request without permission."""
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.get(url)
            self.assertHttpStatus(response, 403)

    def test_get_cupholder(self):
        """Test GET request for a single Cupholder."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        instance = Cupholder.objects.first()
        url = self._get_detail_url(instance)
        response = self.client.get(url)

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['id'], instance.pk)
        self.assertEqual(response.data['name'], instance.name)
        self.assertEqual(response.data['rack']['id'], instance.rack.pk)
        self.assertEqual(response.data['cupholder_type']['id'], instance.cupholder_type.pk)
        self.assertEqual(response.data['mount_face']['value'], instance.mount_face)

    def test_create_cupholder(self):
        """Test POST request to create a Cupholder."""
        self.add_permissions('netbox_cup_holder_plugin.add_cupholder')

        rack = create_rack()
        url = self._get_list_url()
        name = f'API Created {get_random_string(10)}'

        data = {
            'name': name,
            'rack': rack.pk,
            'cupholder_type': self.cupholder_type.pk,
            'mount_face': CupholderMountFaceChoices.FACE_LEFT,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)

        instance = Cupholder.objects.get(name=name)
        self.assertEqual(instance.name, name)
        self.assertEqual(instance.rack, rack)
        self.assertEqual(instance.cupholder_type, self.cupholder_type)
        self.assertEqual(instance.mount_face, CupholderMountFaceChoices.FACE_LEFT)
        self.assertEqual(response.data['id'], instance.pk)

    def test_create_cupholder_without_permission(self):
        """Test POST request without permission."""
        url = self._get_list_url()

        with disable_warnings('django.request'):
            response = self.client.post(
                url,
                {
                    'name': 'Test',
                    'rack': create_rack().pk,
                    'cupholder_type': self.cupholder_type.pk,
                    'mount_face': CupholderMountFaceChoices.FACE_FRONT,
                },
                format='json',
            )
            self.assertHttpStatus(response, 403)

    def test_bulk_create_cupholders(self):
        """Test bulk creation via API."""
        self.add_permissions('netbox_cup_holder_plugin.add_cupholder')

        racks = [create_rack(name=f'Bulk Rack {i}') for i in range(1, 4)]
        url = self._get_list_url()
        data = [
            {
                'name': f'Bulk {i}',
                'rack': racks[i - 1].pk,
                'cupholder_type': self.cupholder_type.pk,
                'mount_face': CupholderMountFaceChoices.FACE_FRONT,
            }
            for i in range(1, 4)
        ]

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 201)
        self.assertEqual(len(response.data), 3)

        for item in data:
            self.assertTrue(
                Cupholder.objects.filter(name=item['name']).exists()
            )

    def test_update_cupholder(self):
        """Test PATCH request to update a Cupholder."""
        self.add_permissions('netbox_cup_holder_plugin.change_cupholder')

        instance = Cupholder.objects.first()
        url = self._get_detail_url(instance)
        new_name = f'Updated {get_random_string(10)}'

        data = {
            'name': new_name,
            'mount_face': CupholderMountFaceChoices.FACE_RIGHT,
        }

        response = self.client.patch(url, data, format='json')
        self.assertHttpStatus(response, 200)

        instance.refresh_from_db()
        self.assertEqual(instance.name, new_name)
        self.assertEqual(instance.mount_face, CupholderMountFaceChoices.FACE_RIGHT)

    def test_update_cupholder_without_permission(self):
        """Test PATCH request without permission."""
        instance = Cupholder.objects.first()
        url = self._get_detail_url(instance)

        with disable_warnings('django.request'):
            response = self.client.patch(url, {'name': 'Test'}, format='json')
            self.assertHttpStatus(response, 403)

    def test_delete_cupholder(self):
        """Test DELETE request to remove a Cupholder."""
        self.add_permissions('netbox_cup_holder_plugin.delete_cupholder')

        instance = Cupholder.objects.first()
        url = self._get_detail_url(instance)

        response = self.client.delete(url)
        self.assertHttpStatus(response, 204)

        self.assertFalse(
            Cupholder.objects.filter(pk=instance.pk).exists()
        )

    def test_delete_cupholder_without_permission(self):
        """Test DELETE request without permission."""
        instance = Cupholder.objects.first()
        url = self._get_detail_url(instance)

        with disable_warnings('django.request'):
            response = self.client.delete(url)
            self.assertHttpStatus(response, 403)

    def test_options_cupholder(self):
        """Test OPTIONS request for list endpoint."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        url = self._get_list_url()
        response = self.client.options(url)

        self.assertHttpStatus(response, 200)

    def test_filter_by_rack_id(self):
        """Test filtering cup holders by rack."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        other_rack = create_rack(name='Other Rack')
        create_cupholder(name='Other Rack Cupholder', rack=other_rack, cupholder_type=self.cupholder_type)

        url = self._get_list_url()
        response = self.client.get(url, {'rack_id': self.rack1.pk})

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_mount_face(self):
        """Test filtering cup holders by mount face."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        url = self._get_list_url()
        response = self.client.get(url, {'mount_face': CupholderMountFaceChoices.FACE_LEFT})

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['mount_face']['value'], CupholderMountFaceChoices.FACE_LEFT)

    def test_filter_by_cupholder_type_id(self):
        """Test filtering cup holders by catalog type."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholder')

        other_type = create_cupholder_type(name='Other Type')
        create_cupholder(
            name='Other Type Cupholder',
            rack=create_rack(name='Type Filter Rack'),
            cupholder_type=other_type,
        )

        url = self._get_list_url()
        response = self.client.get(url, {'cupholder_type_id': other_type.pk})

        self.assertHttpStatus(response, 200)
        self.assertEqual(response.data['count'], 1)


class CupholderAPIValidationTestCase(PluginAPITestCase):
    """Test Cupholder API validation."""

    @classmethod
    def setUpTestData(cls):
        cls.rack = create_rack()
        cls.cupholder_type = create_cupholder_type()

    def setUp(self):
        """Set up each test."""
        super().setUp()
        self.add_permissions('netbox_cup_holder_plugin.add_cupholder')
        self.list_url_name = 'plugins-api:netbox_cup_holder_plugin-api:cupholder-list'

    def test_create_with_empty_name(self):
        """Test that API validates empty name."""
        url = self._get_list_url()
        data = {
            'name': '',
            'rack': self.rack.pk,
            'cupholder_type': self.cupholder_type.pk,
            'mount_face': CupholderMountFaceChoices.FACE_FRONT,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('name', response.data)

    def test_create_with_duplicate_name(self):
        """Test that API validates duplicate names."""
        create_cupholder(name='Duplicate', rack=create_rack(), cupholder_type=self.cupholder_type)

        url = self._get_list_url()
        data = {
            'name': 'Duplicate',
            'rack': self.rack.pk,
            'cupholder_type': self.cupholder_type.pk,
            'mount_face': CupholderMountFaceChoices.FACE_FRONT,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)

    def test_create_with_missing_required_field(self):
        """Test that API validates required fields."""
        url = self._get_list_url()
        data = {}

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('name', response.data)

    def test_create_with_invalid_mount_face(self):
        """Test that API rejects invalid mount faces such as rear."""
        url = self._get_list_url()
        data = {
            'name': 'Invalid Face',
            'rack': self.rack.pk,
            'cupholder_type': self.cupholder_type.pk,
            'mount_face': 'rear',
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
        self.assertIn('mount_face', response.data)

    def test_create_duplicate_rack(self):
        """Test that API rejects a second cup holder on the same rack."""
        create_cupholder(name='Existing', rack=self.rack, cupholder_type=self.cupholder_type)

        url = self._get_list_url()
        data = {
            'name': 'Duplicate Rack',
            'rack': self.rack.pk,
            'cupholder_type': self.cupholder_type.pk,
            'mount_face': CupholderMountFaceChoices.FACE_LEFT,
        }

        response = self.client.post(url, data, format='json')
        self.assertHttpStatus(response, 400)
