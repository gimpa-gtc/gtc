# Generated by Django 4.2.7 on 2023-12-21 07:46

from django.db import migrations, models

import dashboard.models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_application_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='transaction_id',
            field=models.CharField(default=dashboard.models.Payment.generate_transaction_id, max_length=15, unique=True),
        ),
    ]
