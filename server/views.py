from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .serverform import ServerForm, UserForm, PackageForm, ServiceForm, CommandForm, FileSystemForm
from .Base import *
from django.contrib import messages
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
      result, rccode = sshconnection(servername, user, password, command)
      if rccode == 0:
          messages.success(request, f'Success')
      else:
          messages.warning(request, f'Failed')
          return render(request, 'server/monitor.html', {'error': result[0], 'form': form})
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
      users, rccode = sshconnection(servername, user, password, command2)
      if rccode == 0:
          messages.success(request, f'Success')
      else:
          messages.warning(request, f'Failed')
          return render(request, 'server/users.html', {'error': users[0], 'form': form}) 
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
          packages, rccode = sshconnection(servername, user, password, command3)
      elif Options == "Install":
          command3 = ['echo "Installing Package"', 'rpm -qa --last | tail']
          packages, rccode = sshconnection(servername, user, password, command3)
      elif listpackage:
          command3 = ['yum info ' + listpackage]
          packages, rccode = sshconnection(servername, user, password, command3)
      else:
          packages = ["Please select correct option or provide package name"]    
          rccode = 1
      if rccode == 0:
          messages.success(request, f'Success')
      else:
          messages.warning(request, f'Failed')
          return render(request, 'server/packages.html', {'error': packages[0],'form': form})
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
      servicename = form.cleaned_data.get('servicename')
      Options = form.cleaned_data['Options']
      try:
          Options = dict(form.fields['Options'].choices)[Options]
      except KeyError:
          pass
      if servicename:
          command4 = []
          command4.append("service {0} {1}".format(servicename, Options.lower()))
          services, rccode = sshconnection(servername, user, password, command4)
      if rccode == 0:
          messages.success(request, f'Success')
      else:
          messages.warning(request, f'Failed')
          return render(request, 'server/services.html', {'error': services[0],'form': form})
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
      if command and 'shutdown' not in command and 'poweroff' not in command and 'halt' not in command\
and 'init' not in command and 'reboot' not in command:
          command5 = command.split(",")
          commands, rccode = sshconnection(servername, user, password, command5)
      else:
          commands = ['Server power commands are disabled']
          rccode = 1
      if rccode == 0:
          messages.success(request, f'Success')
      else:
          messages.warning(request, f'Failed')
          return render(request, 'server/commands.html', {'error': commands[0], 'form': form})
      return render(request, 'server/commands.html', {
            'commands': commands[:],
            'form': form
            })
  else:
      form = CommandForm()
  return render(request, 'server/commands.html', {'form': form})

def filesystems(request):
  if request.method == 'POST':
    form = FileSystemForm(request.POST)
    if form.is_valid():
      servername = form.cleaned_data.get('server')
      user = form.cleaned_data.get('user')
      password = form.cleaned_data.get('password')
      fileoptions = form.cleaned_data.get('fileoptions')
      Options = form.cleaned_data['Options']
      try:
          Options = dict(form.fields['Options'].choices)[Options]
      except KeyError:
          pass
      if fileoptions:
          if Options == "Delete":
              filesystemoutput, rccode = removeFS(servername, user, password, fileoptions)
          else:
              try:
                  fileoptions = fileoptions.split(":")
                  filesystemoutput, rccode = filesystem(device=fileoptions[0], partition=fileoptions[1], \
pv=fileoptions[2], vg=fileoptions[3], lv=fileoptions[4], fstype=fileoptions[5],\
 size=fileoptions[6], mountpoint=fileoptions[7])
              except Exception as err:
                  filesystemoutput = ['File System details are not provided in below format',\
'DeviceName:PartitionName:PVName:VGName:LVName:FSType:Size:MountPoindt', err]
                  rccode = 1
      else:
          filesystemoutput = ['File Systems details are not provided in below format',\
'DeviceName:PartitionName:PVName:VGName:LVName:FSType:Size:MountPoinst']
          rccode = 1
      if rccode == 0:
          messages.success(request, f'Success')
      else:
          messages.warning(request, f'Failed')
          return render(request, 'server/filesystems.html', {'error': filesystemoutput,'form': form})
      return render(request, 'server/filesystems.html', {
            'filesystemoutput': filesystemoutput[:],
            'form': form
            })
  else:
      form = FileSystemForm()
  return render(request, 'server/filesystems.html', {'form': form})


