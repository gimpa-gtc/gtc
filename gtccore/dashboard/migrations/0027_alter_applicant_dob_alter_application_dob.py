# Generated by Django 4.2.7 on 2024-04-11 08:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0026_applicant_box_address_applicant_dob_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='dob',
            field=models.DateField(default=datetime.date(2024, 4, 11)),
        ),
        migrations.AlterField(
            model_name='application',
            name='dob',
            field=models.DateField(default=datetime.date(2024, 4, 11)),
        ),
    ]