# Generated by Django 3.2.8 on 2021-11-06 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_product_initial_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='initial_price',
            field=models.IntegerField(),
        ),
    ]
