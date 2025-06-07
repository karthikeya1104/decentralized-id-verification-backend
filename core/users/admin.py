from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'public_id', 'role', 'is_staff', 'is_active', 'is_verified_authority')
    list_filter = ('role', 'is_staff', 'is_active', 'is_verified_authority')
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': (
                'public_id',
                'blockchain_address',
                'private_key',
                'role',
                'sector',
                'proof_document',
                'is_verified_authority',
            )
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': (
                'role',
                'sector',
                'proof_document',
            )
        }),
    )
    search_fields = ('username', 'email', 'public_id', 'blockchain_address')
    ordering = ('username',)
