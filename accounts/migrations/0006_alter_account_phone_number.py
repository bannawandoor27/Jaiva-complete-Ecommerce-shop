# Generated by Django 4.1.3 on 2022-11-29 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_address_email_remove_address_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
