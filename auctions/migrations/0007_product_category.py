# Generated by Django 3.2.8 on 2021-11-01 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_rename_year_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='Books', max_length=64),
            preserve_default=False,
        ),
    ]
