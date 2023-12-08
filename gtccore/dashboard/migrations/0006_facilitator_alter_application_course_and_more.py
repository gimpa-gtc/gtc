# Generated by Django 4.2.7 on 2023-11-29 09:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_course_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facilitator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='facilitators')),
                ('specialization', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='application',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.course'),
        ),
        migrations.AlterField(
            model_name='application',
            name='payment_mode',
            field=models.CharField(choices=[('ONLINE', 'online'), ('BANK', 'bank')], default='ONLINE', max_length=20),
        ),
    ]
