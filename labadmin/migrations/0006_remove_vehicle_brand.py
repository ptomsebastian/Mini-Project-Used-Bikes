# Generated by Django 3.2.15 on 2022-10-05 04:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labadmin', '0005_vehicle_brand'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='brand',
        ),
    ]
