#!/usr/bin/python
import paramiko

commandoutput = []
def sshconnection(servername, user, password, command):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  del commandoutput[:]
  for i in command:
    ssh.connect(servername, username=user)
    stdin, stdout, stderr = ssh.exec_command(i)
    commandoutput.append(stdout.read().strip().decode("utf-8"))
  ssh.close
  return commandoutput

