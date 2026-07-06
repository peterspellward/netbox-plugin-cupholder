import django.db.models.deletion
from django.db import migrations, models


def clear_existing_cupholders(apps, schema_editor):
    Cupholder = apps.get_model('netbox_cup_holder_plugin', 'Cupholder')
    Cupholder.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0001_squashed'),
        ('netbox_cup_holder_plugin', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(clear_existing_cupholders, migrations.RunPython.noop),
        migrations.AddField(
            model_name='cupholder',
            name='rack',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='cupholders',
                to='dcim.rack',
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cupholder',
            name='mount_face',
            field=models.CharField(
                choices=[
                    ('front', 'Front'),
                    ('left', 'Left side'),
                    ('right', 'Right side'),
                ],
                max_length=50,
                verbose_name='Mount face',
            ),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='cupholder',
            options={'ordering': ('rack', 'mount_face', 'name'), 'verbose_name_plural': 'Cupholders'},
        ),
    ]
