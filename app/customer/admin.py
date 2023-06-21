from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerCreationForm, CustomUserChangeForm
from .models import Customer,Avatars

class CustomerAdmin(UserAdmin):
    add_form = CustomerCreationForm
    form = CustomUserChangeForm
    model = Customer
    list_display = ('email','first_name','last_name','phone_number','is_superuser','is_staff','is_active')
    list_filter = ('email','first_name','last_name','phone_number','is_superuser','is_staff','is_active')

    fieldsets = (
        (None, {'fields': ('email','password','first_name','last_name','phone_number','avatar')}),
        ("Permissions", {'fields': ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','first_name','last_name','phone_number','avatar','password1','password2','is_staff',
                       'is_active','groups','user_permissions')
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Customer,CustomerAdmin)

class AvatarsAdmin(admin.ModelAdmin):
    
    list_display = ('title','image')
    list_filter = ('title',)

admin.site.register(Avatars,AvatarsAdmin)