from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'country')
    list_filter = ('country',)
    search_fields = ('email', 'first_name', 'last_name', 'country', 'city')
    ordering = ('email',)
    fieldsets = (
        ('Account information', {'fields': ('email', 'password')}),
        ('Personal information', {'fields': ('first_name', 'last_name')}),
        ('Delivery information', {'fields': ('country', 'city', 'address','postal_code')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'user_permissions', 'groups')}),
        ('Important information', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        ('None', {'class': ('wide',), 'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}),
    )
    
    def get_form(self, request, obj = None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'username' in form.base_fields:
            form.base_fields['username'].disabled = True
        return form


admin.site.register(CustomUser, CustomUserAdmin)