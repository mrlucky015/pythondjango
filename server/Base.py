#!/usr/bin/python

# devicename:partitionname:pvname:vgname:lvname:type:size:mountpoint
import paramiko
from datetime import datetime
import os


class FileSystem(object):
    def __init__(self, device=None, partition=None, pv=None, vg=None, lv=None,
                 fstype=None, size=None, mountpoint=None):
        self.device = "/dev/{0}".format(device)
        self.partition = "/dev/{0}".format(partition)
        self.pv = "/dev/{0}".format(pv)
        self.vg = vg
        self.lv = lv
        self.lvname = "/dev/mapper/{0}-{1}".format(vg, lv)
        self.fstype = fstype
        self.size = size
        self.mountpoint = mountpoint

    def getCommands(self):
        commands = {'fdiskcheck': "fdisk -l {0} | grep -i {0}".format(self.device),
                    'partitioncheck': "fdisk -l {0}".format(self.partition),
                    'pvcheck': "pvdisplay {0}".format(self.pv),
                    'vgcheck': "vgdisplay {0}".format(self.vg),
                    'lvcheck': "lvdisplay /dev/mapper/{0}-{1}".format(self.vg, self.lv),
                    'mountpointcheck': "stat {0}".format(self.mountpoint)
                    }
        return commands

    def runChecks(self, commands):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        checksoutput = {}
        try:
            ssh.connect('localhost', username='demouser')
        except Exception:
            pass
        for check, command in commands.items():
            command = "sudo {0}".format(command)
            # stdin, stdout, stderr = ssh.exec_command(command)
            stdin, _, _ = ssh.exec_command(command)
            checksoutput[check] = stdin.channel.recv_exit_status()
            # checksoutput.append(stdout.read().strip().decode("utf-8"))
        ssh.close
        return checksoutput

    def runCommand(self, commands, executionoutput):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect('localhost', username='demouser')
        except Exception:
            commandoutput.append("Please provide valid Server Name or Valid UserName")
            rccode = 1
            return executionoutput, rccode
        for check, command in commands.items():
            command = "sudo {0}".format(command)
            stdin, stdout, stderr = ssh.exec_command(command)
            if stdout.channel.recv_exit_status() == 0:
                executionoutput.append("========================================================\
===========================")
                executionoutput.append("Executing command: {0}\n".format(check))
                executionoutput.append(stdout.read().decode("utf-8"))
                executionoutput.append("{0} command executed successfully\n".format(check))
                rccode = 0
            else:
                executionoutput.append(stderr.read().decode("utf-8"))
                executionoutput.append("Failed to create file system on server Exited")
                rccode = 1
                break
        ssh.close
        return executionoutput, rccode

    def partitionCreate(self):
        return r'echo -e "o\nn\np\n1\n\n\nt\n8e\nw" |sudo fdisk {0}'.format(self.device)

    def physicalVolume(self):
        return 'pvcreate {0} {1}'.format(self.pv, self.partition)

    def volumeGroup(self):
        return 'vgcreate {0} {1}'.format(self.vg, self.pv)

    def logicalVolume(self):
        return 'echo "y" | sudo lvcreate -L +{0} -n {1} {2}'.format(self.size, self.lv, self.vg)

    def formatDisk(self):
        return 'mkfs.xfs {0}'.format(self.lvname)

    def mountPoint(self):
        return 'mkdir -p {0}'.format(self.mountpoint)

    def runMount(self):
        return 'mount {0} {1}'.format(self.lvname, self.mountpoint)

    def backupFstab(self):
        now = datetime.now().strftime("%Y-%m-%d-%H-%M")
        file = '/etc/fstab'
        return 'cp -pr {0} {0}-{1}'.format(file, now)

    def addFstab(self):
        return r'echo -e "{0}  {1} \t\t\t{2}\tdefaults\t0 0" \
        '.format(self.lvname, self.mountpoint, self.fstype)

def sshconnection(servername, user, password, command):
  ssh = paramiko.SSHClient()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  commandoutput = []
  try:
     ssh.connect(servername, username=user)
  except Exception as err:
     commandoutput.append("Please provide valid Server Name or Valid UserName")
     rccode = 1
     return commandoutput, rccode
  for commands in command:
    commands = "sudo {0}".format(commands)
    stdin, stdout, stderr = ssh.exec_command(commands)
    if stdout.channel.recv_exit_status() == 0:
        commandoutput.append(stdout.read().strip().decode("utf-8"))
        rccode = 0
    else:
        commandoutput.append(stderr.read().decode("utf-8"))
        rccode = 1
        break
  ssh.close
  return commandoutput, rccode

def filesystem(**kwargs):
    executecommand = {}
    executionoutput = []
    try:
        fs1 = FileSystem(device=kwargs['device'], partition=kwargs['partition'], \
pv=kwargs['pv'], vg=kwargs['vg'], lv=kwargs['lv'], fstype=kwargs['fstype'], \
size=kwargs['size'], mountpoint=kwargs['mountpoint'])
    except Exception:
        executionoutput.append("Details provided are not valid")
        rccode = 1
        return  executionoutput, rccode
    commands = fs1.getCommands()
    basicchecks = fs1.runChecks(commands)
    for i in basicchecks:
        if basicchecks['lvcheck'] == 0:
            executionoutput.append("We can see File System is Already Available")
            executionoutput.append("Please delete File System using option Delete")
            rccode = 1
            return  executionoutput, rccode
        else:
            continue
    if basicchecks['fdiskcheck'] == 0 and basicchecks['partitioncheck'] == 0:
        executionoutput.append("Disk Exists on server, Partition also exists on server. \
    Proceeding with Physical Volume, Volume Group and Logical Volume creation")
        if basicchecks['pvcheck'] != 0:
            executionoutput.append("Creating Physical Volume, Volume Group and Logical Volume")
            executecommand.update(CreatePV=fs1.physicalVolume())
            executecommand.update(CreateVG=fs1.volumeGroup())
            executecommand.update(CreateLV=fs1.logicalVolume())
            executecommand.update(FormatDISK=fs1.formatDisk())
            if basicchecks['mountpointcheck'] != 0:
                executecommand.update(CreateMountPoint=fs1.mountPoint())
            executecommand.update(MountFS=fs1.runMount())
            executecommand.update(BackupFSTABFile=fs1.backupFstab())
            executecommand.update(FstabEntry=fs1.addFstab())
            executionoutput, rccode = fs1.runCommand(executecommand, executionoutput)
        elif basicchecks['vgcheck'] != 0:
            executionoutput.append("Creating Volume Group and Logical Volume")
            executecommand.update(CreateVG=fs1.volumeGroup())
            executecommand.update(CreateLV=fs1.logicalVolume())
            executecommand.update(FormatDISK=fs1.formatDisk())
            if basicchecks['mountpointcheck'] != 0:
                executecommand.update(CreateMountPoint=fs1.mountPoint())
            executecommand.update(MountFS=fs1.runMount())
            executecommand.update(BackupFSTABFile=fs1.backupFstab())
            executecommand.update(FstabEntry=fs1.addFstab())
            executionoutput, rccode = fs1.runCommand(executecommand, executionoutput)
        elif basicchecks['lvcheck'] != 0:
            executionoutput.append("Creating Logical Volume")
            executecommand.update(CreateLV=fs1.logicalVolume())
            executecommand.update(FormatDISK=fs1.formatDisk())
            if basicchecks['mountpointcheck'] != 0:
                executecommand.update(CreateMountPoint=fs1.mountPoint())
            executecommand.update(MountFS=fs1.runMount())
            executecommand.update(BackupFSTABFile=fs1.backupFstab())
            executecommand.update(FstabEntry=fs1.addFstab())
            executionoutput, rccode = fs1.runCommand(executecommand, executionoutput)
    elif basicchecks['fdiskcheck'] == 0 and basicchecks['partitioncheck'] != 0:
        executionoutput.append("Disk is available, Proceeding with partition creation")
        executecommand.update(CreatePartition=fs1.partitionCreate())
        executecommand.update(CreatePV=fs1.physicalVolume())
        executecommand.update(CreateVG=fs1.volumeGroup())
        executecommand.update(CreateLV=fs1.logicalVolume())
        executecommand.update(FormatDISK=fs1.formatDisk())
        if basicchecks['mountpointcheck'] != 0:
            executecommand.update(CreateMountPoint=fs1.mountPoint())
        executecommand.update(MountFS=fs1.runMount())
        executecommand.update(BackupFSTABFile=fs1.backupFstab())
        executecommand.update(FstabEntry=fs1.addFstab())
        executionoutput, rccode = fs1.runCommand(executecommand, executionoutput)
    else:
        executionoutput.append("Disk is Not available, Please provide correct Disk name")
        rccode = 1

    return executionoutput, rccode

def removeCommand(server, user, password, commands, executionoutput):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    executionoutput = []
    try:
        ssh.connect(server, username=user)
    except Exception:
        executionoutput.append("Please provide valid Server Name or Valid UserName")
        rccode = 1
        return executionoutput, rccode
    for check, command in commands.items():
        command = "sudo {0}".format(command)
        stdin, stdout, stderr = ssh.exec_command(command)
        if stdout.channel.recv_exit_status() == 0:
            executionoutput.append("========================================================\
=======================")
            executionoutput.append("Executing command: {0}\n".format(check))
            executionoutput.append(stdout.read().decode("utf-8"))
            executionoutput.append("{0} command executed successfully\n".format(check))
            rccode = 0
        else:
            if check == 'unmountFS':
                executionoutput.append("File System test is not mounted Proceeding with next steps")
            else:
                executionoutput.append(stderr.read().decode("utf-8"))
                executionoutput.append("Failed to unmount and remove partition on server Exited")
                rccode = 1
                break
    ssh.close
    return executionoutput, rccode

def removeFS(servername, user, password, command):
    executionoutput = []
    executecommand = {}
    executecommand.update(unmountFS='umount /test')
    executecommand.update(removeLV='echo "y"| sudo lvremove /dev/mapper/testvg/testlv')
    executecommand.update(removeVG='vgremove testvg')
    executecommand.update(removePV='pvremove /dev/xvdg1')
    executecommand.update(removePartition=r'echo -e "d\nw" |sudo fdisk /dev/xvdg')
    executionoutput, rccode = removeCommand(servername, user, password , executecommand, executionoutput)
    return executionoutput, rccode

if __name__ == '__main__':
    print("File System Creation Version: 0.0.5")
