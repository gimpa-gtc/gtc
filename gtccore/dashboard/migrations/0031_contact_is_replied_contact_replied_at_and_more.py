# Generated by Django 4.2.7 on 2024-04-22 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0030_alter_applicant_dob_alter_application_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contact',
            name='replied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='replied_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contact',
            name='replied_message',
            field=models.TextField(default=''),
        ),
    ]