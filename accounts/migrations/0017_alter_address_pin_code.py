# Generated by Django 4.1.3 on 2022-12-20 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_address_pin_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='pin_code',
            field=models.IntegerField(null=True),
        ),
    ]