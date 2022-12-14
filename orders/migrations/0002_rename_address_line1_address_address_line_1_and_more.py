# Generated by Django 4.1.3 on 2022-12-16 02:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='address_line1',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='address_line2',
            new_name='address_line_2',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='first_name',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='pincode',
            new_name='pin_code',
        ),
        migrations.RemoveField(
            model_name='address',
            name='email',
        ),
        migrations.RemoveField(
            model_name='address',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='phone',
        ),
    ]
