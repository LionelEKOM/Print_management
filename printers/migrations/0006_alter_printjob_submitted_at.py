# Generated by Django 4.2.11 on 2024-10-06 09:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('printers', '0005_alter_printer_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='printjob',
            name='submitted_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Soumis le'),
        ),
    ]
