# Generated by Django 4.0.3 on 2022-06-16 04:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_faq_service_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='servicerequirement',
            old_name='service',
            new_name='service_req',
        ),
    ]
