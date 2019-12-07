from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ServerForm(forms.Form):
  server = forms.CharField(label='Server name', max_length=100)
  user = forms.CharField(label='User name', max_length=30)
  password = forms.CharField(label='Password', max_length=30, required=False)
  class Meta:
    fields = ['server', 'user', 'password']
    
class UserForm(ServerForm):
  Options = forms.CharField(label='Add User - Provide in ":" delimited Values', max_length=30, required=False)
  class Meta:
    fields = ['server', 'user', 'password', 'Options']

class PackageForm(ServerForm):
  listpackage = forms.CharField(label='Show Package Info', max_length=30, required=False)
  Options = forms.ChoiceField(widget=forms.RadioSelect, choices = [('List', 'List'), 
                                                                   ('Install', 'Install')], required=False)
  class Meta:
    fields = ['server', 'user', 'password', 'listpackage', 'Options']

class ServiceForm(ServerForm):
  servicename = forms.CharField(label='Service Name', max_length=30)
  Options = forms.ChoiceField(widget=forms.RadioSelect, choices = [('Status', 'Status'),
                                                                   ('Start', 'Start'),
                                                                   ('Stop', 'Stop'),
                                                                   ('Restart', 'Restart')], required=True)
  class Meta:
    fields = ['server', 'user', 'password', 'Options']

class CommandForm(ServerForm):
  command = forms.CharField(label='Enter Command to Execute in "," separated', max_length=30, required=True)
  class Meta:
    fields = ['server', 'user', 'password', 'command']

class FileSystemForm(ServerForm):
  fileoptions = forms.CharField(label='Enter FS parameters in ":" Separated form,Please use  \
xvdg:xvdg1:xvdg1:testvg:testlv:xfs:8G:/test for testing', max_length=60, required=True)
  Options = forms.ChoiceField(widget=forms.RadioSelect, choices = [('Delete', 'Delete')], required=False)
  class Meta:
    fields = ['server', 'user', 'password', 'fileoptions']

