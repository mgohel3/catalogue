# Generated by Django 5.0.1 on 2024-01-18 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0011_shop_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='seller.shop'),
        ),
    ]
