# Generated by Django 4.2.3 on 2023-07-22 12:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_alter_reservation_end_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='end_time',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='start_time',
            new_name='start_date',
        ),
    ]