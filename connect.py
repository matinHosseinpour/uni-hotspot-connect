import requests
import platform
import os
from time import sleep
import subprocess
import argparse
import sys

parser = argparse.ArgumentParser(description='Connect or disconnect from the Internet.')

parser.add_argument("-u", "--username", help="Username")
parser.add_argument("-p", "--password", help="Password")
parser.add_argument("-c", "--connect", help="Connect to Internet", action="store_true")
parser.add_argument("-d", "--disconnect", help="Disconnect from Internet", action="store_true")
parser.add_argument("-s", "--status", help="Check connection status", action="store_true")
parser.add_argument("-v", "--vpn", help="Check vpn connection status", action="store_true")

args, unknown = parser.parse_known_args()

username="example"
password="example"
base_url="https://internet.birjand.ac.ir"
dst="https%3A%2F%2Fbirjand.ac.ir"
popup="true"

def get_wifi_list():
    cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-s"]

    output = subprocess.check_output(cmd)

    output_lines = output.decode("utf-8").split("\n")

    wifi_list = []

    for line in output_lines[1:]:
        if line:
            network_name = line.split()[0]
            wifi_list.append(network_name)

    return wifi_list

def change_wifi(network_name, password):
    try:
        if platform.system() == 'Windows':
            os.system('netsh wlan connect name="{}"'.format(network_name))
            
        elif platform.system() == 'Darwin':
            cmd = ["networksetup", "-setairportnetwork", "en0", network_name, password]

            subprocess.check_output(cmd)
        print('connected to ' + network_name + ' wifi')
    except:
        print('error in connect to ' + network_name + ' wifi')

def is_reachable(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200 or response.status_code == 301
    except requests.exceptions.RequestException:
        return False

def wait_for_ping(url):
    try:
        counter = 0
        print('waiting for ' + url + ' ...')
        while not(is_reachable(url)):
            if (counter > 10):
                raise Exception('Ping timeout !, please check your connection')
                
            counter += 1
            sleep(1)
    except:
        print('unable ping ' + url)

def login():
    wait_for_ping('https://birjand.ac.ir/fa')
    try:
        response = requests.post(base_url + '/login', data={'username': username, 'password': password,'dst':dst,'popup':popup})
        if response.status_code == 200:
            if is_reachable('http://google.com'):
                print('connected to Internet')
                return True
    except:
        print('error in connection')
        return False

def logout():
    wait_for_ping('https://birjand.ac.ir/fa')
    try:
        response = requests.get(base_url + '/logout?')
        if response.status_code == 200:
            print('disconnected from Internet')
    except:
        print('error in connection')

def check_connection():
    result = []
    for i in range(0,6):
        print("\rchecking connection status ... (" + str(i * 20) + "%)", end="")
        result.append(is_reachable('http://google.com'))

    sys.stdout.write('\x1b[2K')

    if True in result and False not in result:
        print('\rstatus: connected, quality: Bad')
    elif False in result and True not in result:
        print('\rstatus: disconnected')
    else:
        print('\rstatus: connected, quality: Bad')

def check_vpn_connection():
    result = []
    for i in range(0,11):
        print("\rchecking vpn connection status ... (" + str(i * 10) + "%)", end="")
        result.append(is_reachable('http://youtube.com'))

    sys.stdout.write('\x1b[2K')

    if True in result and False not in result:
        print('\rvpn status: connected, quality: Bad')
    elif False in result and True not in result:
        print('\rvpn status: disconnected')
    else:
        print('\rvpn status: connected, quality: Bad')

def set_user(user):
    global username
    username = user

def set_pass(pwd):
    global password
    password = pwd

if __name__ == '__main__':

    if args.username and args.password:
        set_user(args.username)
    
    if args.password:
        set_pass(args.password)

    if args.connect:
        change_wifi('Network', '')
        if login():
            check_connection()
    
    if args.disconnect:
        logout()

    if args.status:
        check_connection()

    if args.vpn:
        check_vpn_connection()
