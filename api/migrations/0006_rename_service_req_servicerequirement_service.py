# Generated by Django 4.0.3 on 2022-06-16 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_service_servicerequirement_service_req'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicerequirement',
            old_name='service_req',
            new_name='service',
        ),
    ]