#
#   STONE PORT SCAN
#  [ Stolar Studio ]
#

ver = "0.1.7"

import threading
import socket
import os
import sys
import configparser

if not os.path.exists("settings.txt"):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "hosts-file", "false")
    config.set("Settings", "hosts-file-name", "hosts.txt")
    config.set("Settings", "ports-file", "false")
    config.set("Settings", "ports-file-name", "ports.txt")
    config.set("Settings", "thread", "true")
    config.add_section("Visual")
    config.set("Visual", "print-logo", "true")
    config.set("Visual", "progress-bar", "true")
    with open("settings.txt", "w") as config_file:
        config.write(config_file)
try:
    config = configparser.ConfigParser()
    config.read("settings.txt")
    hosts_file = config.get("Settings", "hosts-file")
    hosts_file_name = config.get("Settings", "hosts-file-name")
    ports_file = config.get("Settings", "ports-file")
    ports_file_name = config.get("Settings", "ports-file-name")
    thread = config.get("Settings", "thread")
    print_logo = config.get("Visual", "print-logo")
    progress_bar = config.get("Visual", "progress-bar")
except:
    print("ERROR READ SETTINGS FILE")
    input("\nPress enter...")
    exit()

hosts_file_bool = True if hosts_file == 'true' or hosts_file == 'True' else False
ports_file_bool = True if ports_file == 'true' or ports_file == 'True' else False
thread_bool = True if thread == 'true' or thread == 'True' else False

print_logo_bool = True if print_logo == 'true' or print_logo == 'True' else False
progress_bar_bool = True if progress_bar == 'true' or progress_bar == 'True' else False

if print_logo_bool:
    print("""
   _____ _                     _____           _      _____
  / ____| |                   |  __ \         | |    / ____|
 | (___ | |_ ___  _ __   ___  | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __
  \___ \| __/ _ \| '_ \ / _ \ |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
  ____) | || (_) | | | |  __/ | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |
 |_____/ \__\___/|_| |_|\___| |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|    """)
else:
    print("Stone Port Scanner")
print("Ver : "+ver)
print('-' * 35)

if ports_file_bool and os.path.exists(ports_file_name):
    ports = []
    with open(ports_file_name) as f:
        ports.append(f.read().splitlines())
    print("PORTS : " + ports_file_name + "[ "+str(len(ports[0]))+" ELEMENT ]")
else:
    ports = [[21, 22, 23, 25, 38, 43, 80, 999, 109, 110, 115, 118, 119, 143,
    194, 220, 443, 540, 585, 591, 1112, 1433, 1443, 3128, 3197,
    3306, 4000, 4333, 5100, 5432, 6669, 8000, 8080, 9014, 9200]]
    print("PORTS : DEFAULT")

if hosts_file_bool and os.path.exists(hosts_file_name):
    hosts = []
    with open(hosts_file_name) as f:
        hosts.append(f.read().splitlines())
    print("HOSTS : ", end = '')
    print(' | '.join(hosts[0]))
else:
    target = input('Enter host : ')

print('-' * 35)
open_ports = []

def portscan(port, arr = False):
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s_tcp.settimeout(0.5); s_udp.settimeout(0.5)
    try:
        connection_tcp = s_tcp.connect((target, port))
        if not arr == True:
            print("TCP " + str(target) + " : " + str(port))
        else:
            open_ports.append("TCP " + str(target) + " : " + str(port))
        connection.close()
    except:
        pass
    try:
        connection_udp = s_udp.connect((target, port))
        if not arr == True:
            print("UDP " + str(target) + " : " + str(port))
        else:
            open_ports.append("UDP " + str(target) + " : " + str(port))
        connection.close()
    except:
        pass

def scan_host(target):
    print(target + " START SCANNING")
    for element in ports[0]:
        portscan(int(element))
    print(target + " STOP SCANNING")

def scan_host_multi(target):
    print(target + " START SCANNING")
    if progress_bar_bool:
        pb_i = -2
        pb_max = len(ports[0])
    for element in ports[0]:
        t = threading.Thread(target=portscan, kwargs={'port': int(element), 'arr': True})
        t.start()
        if progress_bar_bool:
            pb_i += 1
            sys.stdout.write('\r')
            part = float(pb_i)/(pb_max - 2)
            symbols_num = int(30 * part)
            sys.stdout.write("SCANNING [%-30s] %3.2f%%" % ('='*symbols_num, part*100))
            sys.stdout.flush()
    if progress_bar_bool:
        sys.stdout.write("\n")
    while True:
        if threading.active_count() < 3:
            if len(open_ports) > 0:
                print('\n'.join(open_ports))
            else:
                print(target + " PORTS ARE NOT OPEN")
            open_ports.clear()
            print(target + " STOP SCANNING")
            break;

if hosts_file_bool:
    for target in hosts[0]:
        if thread_bool:
            scan_host_multi(target)
        else:
            scan_host(target)
else:
    if thread_bool:
        scan_host_multi(target)
    else:
        scan_host(target)

input("\nPress enter...")
