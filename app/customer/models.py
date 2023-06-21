from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager

class Avatars(models.Model):
    title = models.CharField(_("image title"),max_length=100)
    image = models.ImageField(_('avatar'),upload_to='avatars/')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Avatar'

class Customer(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_("first name"),max_length=255)
    last_name = models.CharField(_("last name"), max_length=255)
    phone_number = models.CharField(_('phone number'),max_length=15,blank=True)
    avatar = models.ForeignKey(Avatars,on_delete=models.DO_NOTHING,related_name='customer_avatar',null=True,blank=True)
    favourite_products = models.ManyToManyField('delivery.Product',related_name='user_fav_products')

    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','phone_number']

    objects = CustomUserManager()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self) -> str:
        return self.get_full_name()
    
