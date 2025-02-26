# Generated by Django 4.2.7 on 2024-04-22 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0031_contact_is_replied_contact_replied_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customcourserequest',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customcourserequest',
            name='replied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customcourserequest',
            name='replied_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='customcourserequest',
            name='replied_message',
            field=models.TextField(default=''),
        ),
    ]
