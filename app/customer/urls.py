from django.urls import path,include
from . import views
from django.contrib.auth.urls import urlpatterns

app_name = 'customer'

urlpatterns = [
    path('dashboard/', views.get_dashboard,name='get_dashboard'),
    path('register/', views.register, name='register'),
    path('choose_avatar/', views.choose_avatar, name='choose_avatar'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('give_email_code/',views.give_email_code, name='give_email_code'),
]