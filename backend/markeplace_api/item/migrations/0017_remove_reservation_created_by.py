# Generated by Django 5.0.6 on 2024-06-07 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0016_reservation_details_from_customer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='created_by',
        ),
    ]