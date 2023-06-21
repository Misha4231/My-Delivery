from django.shortcuts import render,redirect
from .models import Customer,Avatars
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import UserRegistrationForm,CustomUserChangeForm
from django.contrib.auth import authenticate, login
import json
import random
from django.core.mail import send_mail
from .tasks import send_email_code

def get_dashboard(request):
    html = render(request,'user/dashboard.html',{'is_manager': request.user.groups.filter(name='Manager').exists}).content.decode('utf-8')
    return JsonResponse({'dashboard_html': html})

def give_email_code(request):
    random_digit = random.randint(10000,99999)
    body = json.loads(request.body.decode('utf-8'))
    email = body['send_email']
    send_email_code.delay(email,random_digit)
    return JsonResponse({'code': random_digit})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            new_user.save()
            login(request=request, user=new_user)
            
            return redirect('home_page')
        else:
            user_form = UserRegistrationForm()
            return render(request,'user/register.html',{'form': user_form})
    else:
        user_form = UserRegistrationForm()
    return render(request,'user/register.html',{'form': user_form})

def choose_avatar(request):
    if request.method == 'POST':
        avatar_id = json.loads(request.body.decode('utf-8'))['choosedId']
        choosed_avatar = Avatars.objects.get(id=int(avatar_id))
        user = Customer.objects.get(email=request.user.email)
        user.avatar = choosed_avatar
        user.save()

        return JsonResponse({'status': 'ok'})
    else:
        avatars = Avatars.objects.all()
        return render(request, 'user/choose_avatar.html',{'avatars':avatars})

def update_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home_page')
        
    form = CustomUserChangeForm(instance=request.user)
    return render(request,'user/update_profile.html',{'form':form})
            