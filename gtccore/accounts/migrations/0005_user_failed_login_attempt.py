# Generated by Django 4.2.7 on 2024-04-23 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='failed_login_attempt',
            field=models.IntegerField(default=0),
        ),
    ]