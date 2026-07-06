"""
Test cases for NetBox Cup Holder Plugin models.
"""

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from ..choices import CupholderMountFaceChoices, CupholderSizeChoices
from ..models import Cupholder, CupholderType
from ..testing import PluginModelTestCase
from ..testing.utils import (
    create_cupholder,
    create_cupholder_type,
    create_rack,
    create_tags,
    get_random_string,
)


class CupholderTypeTestCase(PluginModelTestCase):
    """Test CupholderType catalog."""

    def test_seed_data_count(self):
        """Test that the migration seeds at least 12 cup holder types."""
        self.assertGreaterEqual(CupholderType.objects.count(), 12)

    def test_seed_data_contains_big_joe(self):
        """Test that seeded catalog includes Big Joe 6000."""
        model = CupholderType.objects.get(name='Big Joe 6000')
        self.assertEqual(model.size, CupholderSizeChoices.SIZE_XL)
        self.assertEqual(model.material, 'Brushed Steel')

    def test_create_cupholder_type(self):
        """Test creating a CupholderType instance."""
        model = create_cupholder_type(name='Custom Type', size='l', material='Carbon Fibre')
        self.assertEqual(model.name, 'Custom Type')
        self.assertEqual(model.size, 'l')


class CupholderTestCase(PluginModelTestCase):
    """Test Cupholder model."""

    @classmethod
    def setUpTestData(cls):
        """Set up test data for all tests."""
        cls.cupholder_type = create_cupholder_type(name='Test Type')
        cls.rack1 = create_rack(name='Test Rack 1')
        cls.rack2 = create_rack(name='Test Rack 2')
        cls.rack3 = create_rack(name='Test Rack 3')
        create_cupholder(
            name='Test 1',
            rack=cls.rack1,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_FRONT,
        )
        create_cupholder(
            name='Test 2',
            rack=cls.rack2,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_LEFT,
        )
        create_cupholder(
            name='Test 3',
            rack=cls.rack3,
            cupholder_type=cls.cupholder_type,
            mount_face=CupholderMountFaceChoices.FACE_RIGHT,
        )

    def test_create_cupholder(self):
        """Test creating a Cupholder instance."""
        rack = create_rack()
        name = f'Test {get_random_string(10)}'
        instance = create_cupholder(name=name, rack=rack, cupholder_type=self.cupholder_type)

        self.assertEqual(instance.name, name)
        self.assertEqual(instance.rack, rack)
        self.assertEqual(instance.cupholder_type, self.cupholder_type)
        self.assertEqual(instance.mount_face, CupholderMountFaceChoices.FACE_FRONT)
        self.assertIsNotNone(instance.pk)

    def test_cupholder_str(self):
        """Test Cupholder string representation."""
        instance = Cupholder.objects.first()
        self.assertIn(instance.name, str(instance))
        self.assertIn(str(instance.rack), str(instance))
        self.assertIn(str(instance.cupholder_type), str(instance))

    def test_cupholder_absolute_url(self):
        """Test Cupholder get_absolute_url method."""
        instance = Cupholder.objects.first()
        url = instance.get_absolute_url()

        self.assertIsNotNone(url)
        self.assertIn(str(instance.pk), url)

    def test_cupholder_unique_name(self):
        """Test that Cupholder names must be unique."""
        name = 'Duplicate Name'
        create_cupholder(name=name, rack=create_rack(), cupholder_type=self.cupholder_type)

        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name=name,
                rack=create_rack(),
                cupholder_type=self.cupholder_type,
                mount_face=CupholderMountFaceChoices.FACE_FRONT,
            )
            instance.full_clean()

    def test_one_cupholder_per_rack(self):
        """Test that only one cup holder may be assigned to a rack."""
        with self.assertRaises(IntegrityError):
            Cupholder.objects.create(
                name='Duplicate Rack',
                rack=self.rack1,
                cupholder_type=self.cupholder_type,
                mount_face=CupholderMountFaceChoices.FACE_RIGHT,
            )

    def test_model_to_dict(self):
        """Test model_to_dict helper method."""
        instance = Cupholder.objects.get(name='Test 1')
        data = self.model_to_dict(instance)

        self.assertIn('name', data)
        self.assertEqual(data['name'], instance.name)
        self.assertEqual(data['cupholder_type'], instance.cupholder_type.pk)
        self.assertEqual(data['mount_face'], instance.mount_face)
        self.assertEqual(instance.rack, self.rack1)
        self.assertIn('id', data)

    def test_instance_equal(self):
        """Test assertInstanceEqual helper method."""
        instance = Cupholder.objects.get(name='Test 1')

        self.assertInstanceEqual(
            instance,
            {
                'name': instance.name,
                'id': instance.pk,
                'cupholder_type': instance.cupholder_type.pk,
                'mount_face': instance.mount_face,
            }
        )

    def test_cupholder_with_tags(self):
        """Test Cupholder with tags."""
        tags = create_tags(['important', 'test'])
        instance = Cupholder.objects.first()

        instance.tags.add(*tags)
        instance.save()

        self.assertEqual(instance.tags.count(), 2)
        self.assertIn(tags[0], instance.tags.all())

    def test_query_filter(self):
        """Test filtering Cupholder instances."""
        rack = create_rack()
        test_name = f'FilterTest {get_random_string(10)}'
        create_cupholder(name=test_name, rack=rack, cupholder_type=self.cupholder_type)

        results = Cupholder.objects.filter(name=test_name)
        self.assertEqual(results.count(), 1)
        self.assertEqual(results.first().name, test_name)

    def test_ordering(self):
        """Test Cupholder default ordering."""
        qs = Cupholder.objects.filter(name__in=['Test 1', 'Test 2', 'Test 3'])
        instances = list(qs)
        expected = list(qs.order_by(*Cupholder._meta.ordering))
        self.assertEqual(instances, expected)


class CupholderValidationTestCase(PluginModelTestCase):
    """Test Cupholder validation."""

    @classmethod
    def setUpTestData(cls):
        cls.rack = create_rack()
        cls.cupholder_type = create_cupholder_type()

    def test_empty_name(self):
        """Test that empty name is not allowed."""
        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name='',
                rack=create_rack(),
                cupholder_type=self.cupholder_type,
                mount_face=CupholderMountFaceChoices.FACE_FRONT,
            )
            instance.full_clean()

    def test_name_max_length(self):
        """Test name field max length."""
        long_name = 'x' * 101

        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name=long_name,
                rack=create_rack(),
                cupholder_type=self.cupholder_type,
                mount_face=CupholderMountFaceChoices.FACE_FRONT,
            )
            instance.full_clean()

    def test_missing_rack(self):
        """Test that rack is required."""
        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name='No Rack',
                cupholder_type=self.cupholder_type,
                mount_face=CupholderMountFaceChoices.FACE_FRONT,
            )
            instance.full_clean()

    def test_missing_cupholder_type(self):
        """Test that cup holder type is required."""
        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name='No Model',
                rack=create_rack(),
                mount_face=CupholderMountFaceChoices.FACE_FRONT,
            )
            instance.full_clean()

    def test_missing_mount_face(self):
        """Test that mount face is required."""
        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name='No Face',
                rack=create_rack(),
                cupholder_type=self.cupholder_type,
                mount_face='',
            )
            instance.full_clean()

    def test_invalid_mount_face_rear(self):
        """Test that rear is not a valid mount face."""
        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name='Rear Mount',
                rack=create_rack(),
                cupholder_type=self.cupholder_type,
                mount_face='rear',
            )
            instance.full_clean()

    def test_invalid_mount_face_unknown(self):
        """Test that unknown mount faces are rejected."""
        with self.assertRaises(ValidationError):
            instance = Cupholder(
                name='Bad Face',
                rack=create_rack(),
                cupholder_type=self.cupholder_type,
                mount_face='top',
            )
            instance.full_clean()
