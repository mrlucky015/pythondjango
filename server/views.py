from django.shortcuts import render, redirect

from django.http import HttpResponse
from .monitor import sshconnection
from django.contrib.auth.decorators import login_required
from .serverform import ServerForm
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
    form = ServerForm(request.POST)
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
      form = ServerForm()
  return render(request, 'server/users.html', {'form': form})

