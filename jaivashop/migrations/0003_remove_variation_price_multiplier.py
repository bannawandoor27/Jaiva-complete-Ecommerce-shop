# Generated by Django 4.1.3 on 2022-12-13 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jaivashop', '0002_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='price_multiplier',
        ),
    ]
