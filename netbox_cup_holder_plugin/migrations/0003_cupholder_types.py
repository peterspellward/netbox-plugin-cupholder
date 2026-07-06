import django.db.models.deletion
import netbox.models.deletion
import taggit.managers
import utilities.json
from django.db import migrations, models


CUPHOLDER_TYPES = (
    {
        'name': 'Big Joe 6000',
        'size': 'xl',
        'material': 'Brushed Steel',
        'description': (
            'Built for long maintenance windows. Large enough to keep you going through a full rack rebuild '
            'without another trip to the break room.'
        ),
    },
    {
        'name': 'Queen Elizabeth Refined',
        'size': 's',
        'material': 'Fine Bone China',
        'description': (
            'Reserved for the visitor room or office tea trolley. Not recommended anywhere near raised floors '
            'or cable trays.'
        ),
    },
    {
        'name': 'Italiano Decadence',
        'size': 'xs',
        'material': 'Hand-carved Teak',
        'description': (
            'Precision engineered for a perfect espresso. Popular with technicians who believe coffee should be '
            'measured in quality, not quantity.'
        ),
    },
    {
        'name': 'The Night Shift',
        'size': 'xl',
        'material': 'Powder-coated Aluminium',
        'description': (
            'Designed for overnight maintenance windows. Holds enough coffee to see you through until the '
            'breakfast van arrives.'
        ),
    },
    {
        'name': 'Cable Wrangler',
        'size': 'l',
        'material': 'Stainless Steel',
        'description': (
            'Wide enough to accommodate a mug while simultaneously preventing it from being balanced on top of '
            'a patch panel.'
        ),
    },
    {
        'name': 'Cold Aisle Companion',
        'size': 'm',
        'material': 'Double-wall Insulated Steel',
        'description': (
            'Keeps drinks warm even when you\'re working in the cold aisle for hours on end. Condensation resistant.'
        ),
    },
    {
        'name': 'Hot Aisle Survivor',
        'size': 'm',
        'material': 'Titanium',
        'description': (
            'Heat-resistant construction for those inevitable "five minute" jobs that somehow end up in the hot aisle.'
        ),
    },
    {
        'name': 'The Clean Room',
        'size': 's',
        'material': 'White Ceramic Composite',
        'description': (
            'Easy to sanitise and wipe down. Ideal for controlled environments where everything has a cleaning procedure.'
        ),
    },
    {
        'name': 'Maintenance Special',
        'size': 'xl',
        'material': 'Rugged Polymer',
        'description': (
            'Tough enough to survive being knocked off a crash cart. Field tested against ladders, torque wrenches '
            'and the occasional dropped cage nut.'
        ),
    },
    {
        'name': 'The Contractor',
        'size': 'm',
        'material': 'Stainless Steel',
        'description': (
            'Affordable, dependable and usually the first one borrowed by someone who "just needs it for today."'
        ),
    },
    {
        'name': 'Weekend Warrior',
        'size': 'xxl',
        'material': 'Vacuum Stainless',
        'description': (
            'Extra-large capacity for scheduled outages when the nearest café is closed until Monday morning.'
        ),
    },
    {
        'name': 'The Compliance Edition',
        'size': 'm',
        'material': 'Stainless Steel',
        'description': (
            'Clearly labelled, asset tagged and supplied with a wipe-clean maintenance log. Auditors love it.'
        ),
    },
)


def seed_cupholder_types(apps, schema_editor):
    CupholderType = apps.get_model('netbox_cup_holder_plugin', 'CupholderType')
    for entry in CUPHOLDER_TYPES:
        CupholderType.objects.create(**entry)


def unseed_cupholder_types(apps, schema_editor):
    CupholderType = apps.get_model('netbox_cup_holder_plugin', 'CupholderType')
    CupholderType.objects.filter(
        name__in=[entry['name'] for entry in CUPHOLDER_TYPES]
    ).delete()


def clear_existing_cupholders(apps, schema_editor):
    Cupholder = apps.get_model('netbox_cup_holder_plugin', 'Cupholder')
    Cupholder.objects.all().delete()


def drop_orphaned_catalog_tables(apps, schema_editor):
    """
    Remove catalog tables left behind when superseded migrations were deleted.

    ``migrate zero`` only reverses migrations still present in the graph, so
    tables created by removed migrations (0003_cupholdermodel through 0005)
    can survive and block CreateModel in this migration.
    """
    connection = schema_editor.connection
    existing = set(connection.introspection.table_names())
    orphaned_tables = (
        'netbox_cup_holder_plugin_cupholdertype',
        'netbox_cup_holder_plugin_cupholdermodel',
    )
    with connection.cursor() as cursor:
        for table in orphaned_tables:
            if table in existing:
                cursor.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0140_imageattachment_image_size'),
        ('users', '0015_owner'),
        ('netbox_cup_holder_plugin', '0002_cupholder_rack_mount'),
    ]

    operations = [
        migrations.RunPython(drop_orphaned_catalog_tables, migrations.RunPython.noop),
        migrations.CreateModel(
            name='CupholderType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('custom_field_data', models.JSONField(blank=True, default=dict, encoder=utilities.json.CustomFieldJSONEncoder)),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='description')),
                ('comments', models.TextField(blank=True, verbose_name='comments')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('size', models.CharField(
                    choices=[
                        ('xs', 'XS'),
                        ('s', 'S'),
                        ('m', 'M'),
                        ('l', 'L'),
                        ('xl', 'XL'),
                        ('xxl', 'XXL'),
                    ],
                    max_length=10,
                )),
                ('material', models.CharField(max_length=100)),
                ('owner', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.PROTECT,
                    to='users.owner',
                )),
                ('tags', taggit.managers.TaggableManager(through='extras.TaggedItem', to='extras.Tag')),
            ],
            options={
                'verbose_name': 'cup holder type',
                'verbose_name_plural': 'cup holder types',
                'ordering': ('name',),
            },
            bases=(netbox.models.deletion.DeleteMixin, models.Model),
        ),
        migrations.RunPython(seed_cupholder_types, unseed_cupholder_types),
        migrations.RunPython(clear_existing_cupholders, migrations.RunPython.noop),
        migrations.AddField(
            model_name='cupholder',
            name='cupholder_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='cupholders',
                to='netbox_cup_holder_plugin.cupholdertype',
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cupholder',
            name='rack',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='cupholder',
                to='dcim.rack',
            ),
        ),
        migrations.AlterModelOptions(
            name='cupholder',
            options={'ordering': ('rack', 'name'), 'verbose_name_plural': 'Cupholders'},
        ),
    ]
