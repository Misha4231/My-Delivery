from .models import Customer

def create_profile(backend,user,*args,**kwrags):
    try:
        first_name = user.split(' ')[0]
        last_name = user.split(' ')[1]
    
        Customer.objects.get_or_create(first_name=first_name,last_name=last_name)
    except:
        Customer.objects.get_or_create(first_name=user)
