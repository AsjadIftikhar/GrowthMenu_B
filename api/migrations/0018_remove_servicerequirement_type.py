# Generated by Django 4.0.3 on 2022-06-17 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_filefield_service_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicerequirement',
            name='type',
        ),
    ]
