from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        # fields = ('email',)
        fields = ('username', 'email', 'first_name', 'last_name', 'role')
