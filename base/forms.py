from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User
#from django.contrib.auth.models import User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:#meta data
        model = Room
        fields ='__all__'#create the form based the metadata of the model Room
        exclude  = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'email', 'bio']