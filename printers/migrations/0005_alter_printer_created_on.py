# Generated by Django 4.2.11 on 2024-10-06 09:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0004_remove_printjob_created_at_remove_printjob_file_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printer',
            name='created_on',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date de création'),
        ),
    ]
