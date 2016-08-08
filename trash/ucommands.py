import os
import json
import sys
import re
import subprocess
import socket

def which(key,program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ['PATH'].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

#    return None
#
#
def os_platform():
    fname="c:/Windows/system32/winver.exe"
    fname_two="/usr/bin/uname"
    if os.path.isfile(fname):
        oper_sys="windows"
    if os.path.isfile(fname_two):
        oper_sys="nix"
    else:
        oper_sys="nix"    
    return oper_sys
#
#
#
def jump(key, jump_to, optional_user=''):

    p = re.compile('\$')
    password = p.sub('\044', key['password'])
    output = []

    output.append('#!/usr/bin/env expect'+"\n")
    output.append('set password {'+key['password']+'}'+"\n")
    output.append('spawn -noecho ssh -l '+ optional_user + key['username'] +' -o StrictHostKeyChecking=no -o CheckHostIP=no -o UserKnownHostsFile=/dev/null '+ key['jump']+' ')

    output.append("\n"+'match_max 100000'+"\n")

    output.append('expect {'+"\n")
    output.append('\t-re {} {'+"\n")
    output.append('\t\tsleep .1'+"\n")


    output.append('\t\tsend -- \"ssh -l '+ optional_user +key['username'] +' -o CheckHostIP=no -o UserKnownHostsFile=/dev/null '+ jump_to +' \\r\"'+"\n")


    output.append('\t\texpect {'+"\n")
    output.append('\t\t\t-re {yes} {'+"\n")
    output.append('\t\t\t\tsleep .1'+"\n")
 
    output.append('\t\t\t\tsend -- "yes\\r"'+"\n")
    output.append('\t\t\t\tsleep .1'+"\n")
    output.append('\t\t\t}'+"\n")
    output.append('\t}'+"\n")
    output.append('\t\texpect {'+"\n")
    output.append('\t\t\t-re {[P|p]assword:} {\r'+"\n")
    output.append('\t\t\t\tsleep .2'+"\n")
    output.append('\t\t\t\tsend -- \"$password\\r\"\r'+"\n")
    output.append('\t\t\t\tsleep .1'+"\n")
    output.append('\t\t\t}'+"\n")
    output.append('\t\t\t}'+"\n")
    output.append('trap { stty rows [stty rows] columns [stty columns] < $spawn_out(slave,name)} WINCH'+"\n")


    output.append('interact {'+"\n")
    output.append('\t\\034 exit'+"\n")
    output.append('}'+"\n")
    output.append('}'+"\n")
    output.append('}'+"\n")
    

    name = 'trash'
    confdir = '{0}'.format(os.path.expanduser('~'))
    script_path = '{0}/{1}.sh'.format(confdir, name)
    fh = open(script_path, 'w')
    fh.write("".join(output))
    fh.close()
    os.chmod(script_path, 448)

    subprocess.call(script_path)

