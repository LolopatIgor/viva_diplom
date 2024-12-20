from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from users.models import User


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'phone', 'password1', 'password2')


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'avatar')
