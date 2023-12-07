# Generated by Django 4.2.7 on 2023-12-07 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_alter_payment_application'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cohort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_month', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
