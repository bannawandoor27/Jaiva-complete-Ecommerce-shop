# Generated by Django 4.1.3 on 2022-12-13 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jaivashop', '0002_variation'),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='jaivashop.variation'),
        ),
    ]
