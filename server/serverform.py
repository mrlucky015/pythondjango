from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ServerForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30)
  Options = forms.CharField(label='List/Add User', max_length=30)
  class Meta:
    fields = ['server', 'user', 'password', 'Options']
    
