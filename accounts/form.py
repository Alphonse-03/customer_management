from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'

class OrderFormEdit(ModelForm):
    class Meta:
        model=Order
        fields=['status']

class OrderFormCreate(ModelForm):
    class Meta:
        model=Order
        fields='__all__'


class CustomerForm(ModelForm):
    class Meta:
        model=Customer
        fields='__all__'
        exclude=['user']
  

class RegistraionForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']
