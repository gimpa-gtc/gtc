# Generated by Django 4.2.7 on 2024-05-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_notification_is_broadcasted'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='fprice_currency',
            field=models.CharField(default='USD', max_length=10),
        ),
    ]