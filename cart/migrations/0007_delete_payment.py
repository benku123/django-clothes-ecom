# Generated by Django 4.0 on 2022-05-27 14:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_merge_0003_alter_product_price_0005_delete_newsletter'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
