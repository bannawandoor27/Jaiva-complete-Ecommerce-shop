# Generated by Django 4.1.3 on 2023-01-04 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jaivashop', '0008_contactmessage_sent_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(),
        ),
    ]
