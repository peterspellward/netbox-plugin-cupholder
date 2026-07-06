"""
Test cases for NetBox Cup Holder Plugin GraphQL API.
"""
from ..choices import CupholderMountFaceChoices
from ..models import Cupholder, CupholderType
from ..testing import PluginGraphQLTestCase
from ..testing.utils import create_cupholder, create_cupholder_type, create_rack


class CupholderGraphQLTestCase(PluginGraphQLTestCase):
    """Test Cupholder GraphQL queries."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        cls.cupholder_type = create_cupholder_type(name='GraphQL Type', size='l', material='Steel')
        cls.rack = create_rack(name='GraphQL Rack')
        create_cupholder(
            name='GraphQL Test 1',
            rack=cls.rack,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_FRONT,
        )

    def test_query_cupholder(self):
        """Test GraphQL query for a single Cupholder."""
        self.add_permissions(
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
            'dcim.view_rack',
        )

        instance = Cupholder.objects.first()

        query = (
            "query { "
            "cupholder(id: " + str(instance.pk) + ") { "
            "id name mount_face "
            "rack { id name } "
            "cupholder_type { id name size material } "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['cupholder']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)
        self.assertEqual(data['mount_face'], instance.mount_face)
        self.assertEqual(data['rack']['id'], str(instance.rack.pk))
        self.assertEqual(data['cupholder_type']['name'], instance.cupholder_type.name)

    def test_query_cupholder_list(self):
        """Test GraphQL query for list of Cupholders."""
        self.add_permissions(
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
            'dcim.view_rack',
        )

        query = """
        query {
            cupholder_list {
                id
                name
                mount_face
                rack {
                    id
                }
                cupholder_type {
                    id
                    name
                }
            }
        }
        """

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['cupholder_list']
        self.assertEqual(len(data), 1)
        self.assertIn('cupholder_type', data[0])

    def test_query_cupholder_type_list(self):
        """Test GraphQL query for cup holder type catalog."""
        self.add_permissions('netbox_cup_holder_plugin.view_cupholdertype')

        query = """
        query {
            cupholder_type_list {
                id
                name
                size
                material
            }
        }
        """

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['cupholder_type_list']
        self.assertGreaterEqual(len(data), 12)
        self.assertTrue(any(item['name'] == 'Hot Aisle Survivor' for item in data))

    def test_query_cupholder_with_all_fields(self):
        """Test GraphQL query with all available fields."""
        self.add_permissions(
            'netbox_cup_holder_plugin.view_cupholder',
            'netbox_cup_holder_plugin.view_cupholdertype',
            'dcim.view_rack',
        )

        instance = Cupholder.objects.first()

        query = (
            "query { "
            "cupholder(id: " + str(instance.pk) + ") { "
            "id name mount_face created last_updated "
            "rack { id name } "
            "cupholder_type { id name size material } "
            "} "
            "}"
        )

        response = self.execute_query(query)
        self.assertIsNone(response.get('errors'))

        data = response['data']['cupholder']
        self.assertEqual(data['id'], str(instance.pk))
        self.assertEqual(data['name'], instance.name)
        self.assertEqual(data['mount_face'], instance.mount_face)
        self.assertIsNotNone(data['created'])
        self.assertIsNotNone(data['last_updated'])
        self.assertEqual(data['rack']['name'], instance.rack.name)
        self.assertEqual(data['cupholder_type']['material'], instance.cupholder_type.material)
