# Generated by Django 4.1.3 on 2022-12-13 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jaivashop', '0004_wishlist_wishlistitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlistitem',
            name='wishlist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='jaivashop.wishlist'),
        ),
    ]
