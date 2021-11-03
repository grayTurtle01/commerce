# Generated by Django 3.2.8 on 2021-11-03 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20211103_1323'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='users',
        ),
        migrations.AddField(
            model_name='user',
            name='watch_list',
            field=models.ManyToManyField(blank=True, related_name='favorites', to='auctions.Product'),
        ),
    ]
