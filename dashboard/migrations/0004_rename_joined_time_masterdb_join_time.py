# Generated by Django 4.2.16 on 2024-10-31 02:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_masterdb_delete_participant_delete_registration'),
    ]

    operations = [
        migrations.RenameField(
            model_name='masterdb',
            old_name='joined_time',
            new_name='join_time',
        ),
    ]
