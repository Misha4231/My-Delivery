# Generated by Django 4.2.2 on 2023-06-20 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0007_remove_order_full_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Review',
        ),
    ]