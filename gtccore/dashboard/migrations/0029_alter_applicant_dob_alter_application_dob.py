# Generated by Django 4.2.7 on 2024-04-18 12:54

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0028_alter_applicant_dob_alter_application_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='dob',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 12, 54, 2, 952256, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='application',
            name='dob',
            field=models.DateField(default=datetime.datetime(2024, 4, 18, 12, 54, 2, 951257, tzinfo=datetime.timezone.utc)),
        ),
    ]
