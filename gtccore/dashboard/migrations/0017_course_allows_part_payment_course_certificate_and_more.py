# Generated by Django 4.2.7 on 2023-12-18 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_payment_receipt'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='allows_part_payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='certificate',
            field=models.FileField(blank=True, null=True, upload_to='certificates'),
        ),
        migrations.AddField(
            model_name='course',
            name='requires_certificate',
            field=models.BooleanField(default=False),
        ),
    ]