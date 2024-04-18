# Generated by Django 4.2.7 on 2024-04-18 13:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_alter_applicant_dob_alter_application_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='application',
            name='dob',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
