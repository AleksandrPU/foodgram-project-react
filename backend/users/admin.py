from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Subscription, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_joined',
        'role'
    )
    list_filter = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Личные данные', {'fields': ('first_name', 'last_name')}),
        ('Доступ',
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'role')}),
        ('Статистика', {'fields': ('date_joined', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
            )
        }),
    )
    search_fields = ('email', 'username',)
    ordering = ('email', 'username',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
