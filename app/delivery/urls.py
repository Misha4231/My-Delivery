from django.urls import path
from . import views

app_name = 'delivery'

urlpatterns = [
    path('products/<str:is_favourite>/',views.products_list,name='products'),
    path('products/<str:is_favourite>/',views.products_list,name='fav_products'),
    path('product_detail/<slug:slug>/',views.product_detail,name='product_detail'),
    path('add_to_favourite/<str:slug>/<str:action>/',views.add_to_favourite, name='add_to_favourite'),
    path('add_to_cart/<slug:slug>/',views.add_to_cart,name="add_to_cart"),
    path('create/', views.order_create,name='order_create'),
    path('order_list/', views.order_list, name='order_list'),
    path('manager_orders/', views.orders_control, name='orders_control'),
    path('change_status/<uuid:order_id>/', views.change_status, name='change_status'),
]