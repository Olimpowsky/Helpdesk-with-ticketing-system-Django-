from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets, 
        (                      
            'User Type',  
            {
                'fields': (
                    'is_customer',
                    'is_engineer'
                ),
            },
        ),
    )
admin.site.register(User, CustomUserAdmin)