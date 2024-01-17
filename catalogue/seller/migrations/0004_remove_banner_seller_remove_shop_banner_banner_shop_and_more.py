# Generated by Django 5.0.1 on 2024-01-12 05:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0003_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='shop',
            name='banner',
        ),
        migrations.AddField(
            model_name='banner',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.shop'),
        ),
        migrations.AddField(
            model_name='shop',
            name='banners',
            field=models.ManyToManyField(blank=True, related_name='shops', to='seller.banner'),
        ),
    ]