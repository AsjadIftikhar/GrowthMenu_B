# Generated by Django 4.0.3 on 2022-07-17 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_rename_hint_servicerequirement_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filefield',
            name='upload_file',
            field=models.FileField(null=True, upload_to='store/files'),
        ),
        migrations.AlterField(
            model_name='imagefield',
            name='upload_image',
            field=models.ImageField(null=True, upload_to='store/images'),
        ),
        migrations.AlterField(
            model_name='textfield',
            name='text',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
