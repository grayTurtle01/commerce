# Generated by Django 3.2.8 on 2021-11-01 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imgage',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]
