# Generated by Django 3.2.8 on 2021-11-03 18:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='date',
        ),
    ]
