# Generated by Django 5.0.1 on 2024-01-18 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0010_category_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='Category',
            field=models.ManyToManyField(blank=True, related_name='shops', to='seller.category'),
        ),
    ]