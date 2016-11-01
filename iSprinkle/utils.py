import os
from subprocess import check_output
from datetime import timedelta


def get_lan_ip():
    stdout = [s[5:] for s in check_output(['ifconfig']).decode().split() if
              len(s) > 5 and "addr:" in s and "127" not in s]
    if len(stdout):
        return stdout[0]
    return 'Error finding LAN IP.'


def uptime():
    stdout = [s for s in check_output(['uptime']).decode().split(',')]
    return ''.join(stdout)


def restart():
    os.system('sudo shutdown -r now')

