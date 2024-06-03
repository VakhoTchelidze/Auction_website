from django.forms import ModelForm
from .models import Item, User
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'is_artist']

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'picture', 'name', 'price', 'description']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'bio', 'is_artist']