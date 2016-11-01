import os
from subprocess import check_output
from datetime import timedelta


def get_lan_ip():
    stdout = [s[5:] for s in check_output(['/sbin/ifconfig']).decode().split() if
              len(s) > 5 and "addr:" in s and "127" not in s]
    if len(stdout):
        return stdout[0]
    return 'Error finding LAN IP.'


def restart():
    os.system('sudo shutdown -r now')


def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(timedelta(seconds=uptime_seconds))
        return uptime_string.split('.')[0]
