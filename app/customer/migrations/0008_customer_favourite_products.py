# Generated by Django 4.2.2 on 2023-06-13 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0004_alter_order_full_price'),
        ('customer', '0007_alter_avatars_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='favourite_products',
            field=models.ManyToManyField(related_name='user_fav_products', to='delivery.product'),
        ),
    ]