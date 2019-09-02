from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ServerForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30, required=False)
  class Meta:
    fields = ['server', 'user', 'password']
    
class UserForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30, required=False)
  Options = forms.CharField(label='Add User - Provide in ":" delimited Values', max_length=30, required=False)
  class Meta:
    fields = ['server', 'user', 'password', 'Options']

class PackageForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30, required=False)
  listpackage = forms.CharField(label='Show Package Info', max_length=30, required=False)
  Options = forms.CharField(label='Install Package', max_length=30, required=False)
  class Meta:
    fields = ['server', 'user', 'password', 'listpackage', 'Options']

class ServiceForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30, required=False)
  Options = forms.CharField(label='Service Name Start/Stop/Restart/Status', max_length=30)
  class Meta:
    fields = ['server', 'user', 'password', 'Options']

class CommandForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30, required=False)
  command = forms.CharField(label='Enter Command to Execute in "," separated', max_length=30, required=False)
  class Meta:
    fields = ['server', 'user', 'password', 'command']

