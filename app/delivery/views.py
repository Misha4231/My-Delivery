from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import Product,OrderItem,Order
from cart.models import Cart
from django.http import HttpResponse,JsonResponse
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import OrderCreateForm,StatusChangeForm
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.conf import settings
import redis
from .tasks import wait_and_delete_status

r = redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,decode_responses=True)


@user_passes_test(lambda user: user.groups.filter(name='Manager').exists())
@require_POST
def change_status(request,order_id):
    form = StatusChangeForm(request.POST)
    if form.is_valid():
        status = form.cleaned_data['status']
        r.set(f'order:{order_id}:status',status)
        if status == 'Ready':
            wait_and_delete_status.delay(f'order:{order_id}:status')
    
    return redirect('delivery:orders_control')

@user_passes_test(lambda user: user.groups.filter(name='Manager').exists())
def orders_control(request):

    cache_keys = r.keys(search='order:*:status')
    process_order_keys = []
    for ck in range(len(cache_keys)):
        try:
            if r.get(cache_keys[ck]) != 'Ready':
                try:
                    process_order_keys.append(cache_keys[ck].split(':')[1])
                except:
                    continue
            else:
                continue
        except:
            continue
    
    orders = Order.objects.filter(id__in=process_order_keys)
    return render(request,'orders/manager_list.html',{'orders':orders})

@login_required
def order_list(request):
    orders = Order.objects.filter(email=request.user.email)

    process_orders = []
    unprocessed_orders = []
    for order in orders:
        order_status = r.get(f'order:{order.id}:status')
        
        if order_status != 'Ready':
            process_orders.append(order)
        else:
            unprocessed_orders.append(order)

    return render(request, 'orders/list.html', {'process_orders': process_orders,'unprocessed_orders':unprocessed_orders})
    

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            if form.cleaned_data['pay_type'] == 'card':
                #Ошибка с jSON not serializeble object !!!!   request.session['order_id'] = order.id
                
                return redirect(reverse('payment:process',args=[order.id]))
            
            order.set_status('Queue')
            print(order.get_status())
            return render(request,'orders/created.html',{'order':order})

    else:
        form = OrderCreateForm()
    
    return render(request,'orders/create.html',{'form':form})

def home_page(request):
    return render(request,'delivery/homePage.html')

def products_list(request,is_favourite):
    if is_favourite == 'true':
        if request.user.is_authenticated:
            products = request.user.favourite_products.all()
            if len(products) == 0:
                return render(request,'delivery/products/list.html',{'is_null':True})
        else:
            return redirect('login')
    else:
        products = Product.objects.all()

    from_price = request.GET.get('from_price')
    to_price = request.GET.get('to_price')

    if from_price:
        products = products.filter(price__gt=from_price)
    if to_price:
        products = products.filter(price__lte=to_price)

    query = request.GET.get('query')
    language = request.LANGUAGE_CODE
    if query:
        products = products.filter(translations__language_code=language,translations__title__contains=query)

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    products_only = request.GET.get('products_only')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        if products_only:
            return HttpResponse('')
        products = paginator.page(paginator.num_pages)

    if products_only:
        return render(request,'delivery/products/products_list.html',{'products': products})
    return render(request,'delivery/products/list.html',{'products': products,'from_price':from_price,'to_price':to_price,'is_null':False})

def product_detail(request, slug):
    product = get_object_or_404(Product,slug=slug)
    return render(request,'delivery/products/detail.html',{'product':product})


def add_to_favourite(request,slug,action):
    product = Product.objects.get(slug=slug)
    if action == 'like':
        request.user.favourite_products.add(product)
    else:
        request.user.favourite_products.remove(product)
    request.user.save()
    return JsonResponse({'status':'ok'})


def add_to_cart(request,slug):
    product = Product.objects.get(slug=slug)
    cart = Cart(request)
    cart.add(product)

    return JsonResponse({'status':'ok'})

