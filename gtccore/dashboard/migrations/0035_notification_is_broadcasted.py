# Generated by Django 4.2.7 on 2024-04-23 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0034_coursecategory_coordinator_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_broadcasted',
            field=models.BooleanField(default=False),
        ),
    ]