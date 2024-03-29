# Generated by Django 4.0.6 on 2022-08-19 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_alter_cart_id_alter_servicerequirement_type_cartitem'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='orderitem',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='form',
            name='order_item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='forms', to='api.orderitem'),
        ),
        migrations.CreateModel(
            name='TextField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=1000, null=True)),
                ('form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='text_field', to='api.form')),
            ],
        ),
        migrations.CreateModel(
            name='ImageField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_image', models.ImageField(null=True, upload_to='store/images')),
                ('form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_field', to='api.form')),
            ],
        ),
        migrations.CreateModel(
            name='FileField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_file', models.FileField(null=True, upload_to='store/files')),
                ('form', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='file_field', to='api.form')),
            ],
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
    ]
