# Generated by Django 4.2.5 on 2024-10-16 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theaters', '0002_alter_performance_duration_alter_performance_theater'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance',
            name='duration',
        ),
        migrations.AddField(
            model_name='performance',
            name='duration_minutes',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
