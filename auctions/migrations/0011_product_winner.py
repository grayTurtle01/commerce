# Generated by Django 3.2.8 on 2021-11-02 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_product_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='winner',
            field=models.CharField(default='"admin"', max_length=64),
        ),
    ]
