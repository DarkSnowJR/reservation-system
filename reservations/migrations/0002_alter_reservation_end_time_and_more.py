# Generated by Django 4.2.3 on 2023-07-22 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_time',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_time',
            field=models.DateField(),
        ),
    ]