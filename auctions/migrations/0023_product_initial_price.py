# Generated by Django 3.2.8 on 2021-11-06 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_delete_bidform'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='initial_price',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
    ]
