# Generated by Django 3.2.8 on 2021-11-01 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_imgage_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_url',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
