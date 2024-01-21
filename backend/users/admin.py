from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'role')
    list_filter = ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
