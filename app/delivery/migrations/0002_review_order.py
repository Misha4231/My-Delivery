# Generated by Django 4.2.2 on 2023-06-13 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=250, verbose_name='topic')),
                ('text', models.TextField(verbose_name='review')),
                ('mark', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='review_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('pay_type', models.CharField(choices=[('card', 'By card'), ('cash', 'By cash')], max_length=7, verbose_name='pay type')),
                ('address', models.CharField(max_length=1000, verbose_name='address')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('products', models.ManyToManyField(related_name='order_products', to='delivery.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_order', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]