"""
Users app admin configuration.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Address


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    fields = ['label', 'street', 'city', 'state', 'postal_code', 'country', 'is_default']
    readonly_fields = []


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'name', 'phone', 'is_admin', 'is_email_verified', 'is_active', 'date_joined']
    list_filter = ['is_admin', 'is_email_verified', 'is_active', 'date_joined']
    search_fields = ['email', 'name', 'phone']
    ordering = ['-date_joined']
    readonly_fields = ['id', 'date_joined', 'updated_at', 'last_login']
    inlines = [AddressInline]

    fieldsets = (
        (None, {'fields': ('id', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'phone', 'avatar_url')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_staff', 'is_superuser', 'is_email_verified', 'groups', 'user_permissions')}),
        ('Timestamps', {'fields': ('date_joined', 'last_login', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_admin', 'is_staff'),
        }),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'state', 'country', 'is_default', 'created_at']
    list_filter = ['country', 'is_default']
    search_fields = ['user__email', 'user__name', 'street', 'city', 'postal_code']
    readonly_fields = ['id', 'created_at', 'updated_at']
    raw_id_fields = ['user']
