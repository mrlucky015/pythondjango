from django.shortcuts import render, redirect
from django.http import HttpResponse
from .monitor import sshconnection
from django.contrib.auth.decorators import login_required
from .serverform import ServerForm, UserForm, PackageForm, ServiceForm, CommandForm
# Create your views here.


def about(request):
  context = {
   'title': 'About'
  }
  return render(request, 'server/about.html', context)
def monitorserver(request):
  if request.method == 'POST':
    form = ServerForm(request.POST)
    if form.is_valid():
      servername = form.cleaned_data.get('server')
      user = form.cleaned_data.get('user')
      password = form.cleaned_data.get('password')
      command = ['date', 'uptime', 'vmstat', 'df -Ph', 'free -m']
      result = sshconnection(servername, user, password, command)
      return render(request, 'server/monitor.html', {
            'date': result[0],
            'uptime': result[1],
            'vmstat': result[2],
            'filesystem': result[3],
            'memory': result[4],
	    'form': form
	    })
  else:
      form = ServerForm()
  return render(request, 'server/monitor.html', {'form': form})

def users(request):
  if request.method == 'POST':
    form = UserForm(request.POST)
    if form.is_valid():
      servername = form.cleaned_data.get('server')
      user = form.cleaned_data.get('user')
      password = form.cleaned_data.get('password')
      command2 = ['cat /etc/passwd | awk -F ":" \'{if($3 >= 1000) print $1}\'', 'cat /etc/group | awk -F ":" \'{if($3 >= 1000) print $1}\'']
      users = sshconnection(servername, user, password, command2)
      return render(request, 'server/users.html', {
            'users': users[0],
	    'group': users[1],
            'form': form
            })
  else:
      form = UserForm()
  return render(request, 'server/users.html', {'form': form})

def packages(request):
  if request.method == 'POST':
    form = PackageForm(request.POST)
    if form.is_valid():
      servername = form.cleaned_data.get('server')
      user = form.cleaned_data.get('user')
      password = form.cleaned_data.get('password')
      listpackage = form.cleaned_data.get('listpackage')
      Options = form.cleaned_data['Options']
      try:
          Options = dict(form.fields['Options'].choices)[Options]
      except KeyError:
          pass
      if Options == "List":
          command3 = ['rpm -qa --last | head']
      elif Options == "Install":
          command3 = ['echo "Installing Package"', 'rpm -qa --last | tail']
      if listpackage:
          command3 = ['yum info ' + listpackage]
      packages = sshconnection(servername, user, password, command3)
      return render(request, 'server/packages.html', {
            'packages': packages[0],
            'form': form
            })
  else:
      form = PackageForm()
  return render(request, 'server/packages.html', {'form': form})

def services(request):
  if request.method == 'POST':
    form = ServiceForm(request.POST)
    if form.is_valid():
      servername = form.cleaned_data.get('server')
      user = form.cleaned_data.get('user')
      password = form.cleaned_data.get('password')
      options = form.cleaned_data.get('Options')
      if options:
          command4 = ['service ' +options+' status']
          services = sshconnection(servername, user, password, command4)
      return render(request, 'server/services.html', {
            'services': services[0],
            'form': form
            })
  else:
      form = ServiceForm()
  return render(request, 'server/services.html', {'form': form})


def commands(request):
  if request.method == 'POST':
    form = CommandForm(request.POST)
    if form.is_valid():
      servername = form.cleaned_data.get('server')
      user = form.cleaned_data.get('user')
      password = form.cleaned_data.get('password')
      command = form.cleaned_data.get('command')
      if command:
          command5 = command.split(",")
          commands = sshconnection(servername, user, password, command5)
      else:
          commands = ['Please Enter Command']
      return render(request, 'server/commands.html', {
            'commands': commands[:],
            'form': form
            })
  else:
      form = CommandForm()
  return render(request, 'server/commands.html', {'form': form})

