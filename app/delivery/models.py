from django.urls import reverse
from django.db import models
from customer.models import Customer
from django.utils.translation import gettext_lazy as _
import uuid
from parler.models import TranslatableModel, TranslatedFields
from django.conf import settings
import redis

r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)

class Product(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("title"),max_length=300),
    )
    
    slug = models.CharField(_("slug"),max_length=300)
    price = models.DecimalField(_("price"),max_digits=10,decimal_places=2)
    max_time = models.PositiveIntegerField(_('max time'))
    image = models.ImageField(_('image'), upload_to='products/')

    def __str__(self) -> str:
        return str(self.slug)
    
    def get_absolute_url(self):
        return reverse('delivery:product_detail',args=[self.slug])



class Order(models.Model):
    PAY_TYPE_COOICES = [
        ('card','By card'),
        ('cash','By cash'),
    ]

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    products = models.ManyToManyField(Product,related_name='order_products')
    pay_type = models.CharField(_('pay type'),max_length=7,choices=PAY_TYPE_COOICES)
    address = models.CharField(_('address'),max_length=1000)
    created = models.DateTimeField(_('created'),auto_now_add=True)
    

    def __str__(self) -> str:
        return f'Order from {self.first_name} {self.last_name}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_status(self):
        cache_key = f'order:{self.id}:status'
        return r.get(cache_key)
    
    def set_status(self,value):
        cache_key = f'order:{self.id}:status'
        r.set(cache_key,value)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return str(self.price)
    
    def get_cost(self):
        return self.price * self.quantity

