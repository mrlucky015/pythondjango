#!/usr/bin/python
import paramiko

a = []
def sshconnection(servername, user, password, command):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  del a[:]
  for i in command:
    ssh.connect(servername, username=user)
    stdin, stdout, stderr = ssh.exec_command(i)
    a.append(stdout.read().rstrip().decode("utf-8"))
  ssh.close
  return a

