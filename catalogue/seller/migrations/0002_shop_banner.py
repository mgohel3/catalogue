# Generated by Django 5.0 on 2024-01-11 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='shop_banners/%Y/%m/%d/'),
        ),
    ]
