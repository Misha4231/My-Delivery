# Generated by Django 4.2.2 on 2023-06-13 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='title')),
                ('slug', models.CharField(max_length=300, verbose_name='slug')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='price')),
                ('max_time', models.PositiveIntegerField(verbose_name='max time')),
                ('image', models.ImageField(upload_to='products/', verbose_name='image')),
            ],
        ),
    ]