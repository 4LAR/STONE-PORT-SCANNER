#
#   STONE PORT SCAN
#  [ Stolar Studio ]
#

ver = "0.1.4"

import threading 
import socket
import os
import configparser
#import argparse

if not os.path.exists("settings.txt"):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "hosts-file", "false")
    config.set("Settings", "hosts-file-name", "hosts.txt")
    config.set("Settings", "ports-file", "false")
    config.set("Settings", "ports-file-name", "ports.txt")
    config.add_section("Visual")
    config.set("Visual", "print-logo", "true")
    #config.set("Visual", "print-ports", "false")
    #config.set("Visual", "progress-bar", "true")
    with open("settings.txt", "w") as config_file:
        config.write(config_file)
try:
    config = configparser.ConfigParser()
    config.read("settings.txt")
    hosts_file = config.get("Settings", "hosts-file")
    hosts_file_name = config.get("Settings", "hosts-file-name")
    ports_file = config.get("Settings", "ports-file")
    ports_file_name = config.get("Settings", "ports-file-name")
    print_logo = config.get("Visual", "print-logo")
    #print_ports = config.get("Visual", "print-ports")
    #progress_bar = config.get("Visual", "progress-bar")
except:
    print("ERROR READ SETTINGS FILE")
    input("\nPress enter...")
    exit()

hosts_file_bool = True if hosts_file == 'true' or hosts_file == 'True' else False
ports_file_bool = True if ports_file == 'true' or ports_file == 'True' else False

print_logo_bool = True if print_logo == 'true' or print_logo == 'True' else False
#print_ports_bool = True if print_ports == 'true' or print_ports == 'True' else False
#progress_bar_bool = True if progress_bar == 'true' or progress_bar == 'True' else False

if print_logo_bool:
    print("""
       _____ _                     _____           _      _____                                 
      / ____| |                   |  __ \         | |    / ____|                                
     | (___ | |_ ___  _ __   ___  | |__) |__  _ __| |_  | (___   ___ __ _ _ __  _ __   ___ _ __ 
      \___ \| __/ _ \| '_ \ / _ \ |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
      ____) | || (_) | | | |  __/ | |  | (_) | |  | |_   ____) | (_| (_| | | | | | | |  __/ |   
     |_____/ \__\___/|_| |_|\___| |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|_| |_|\___|_|                                                                                                                                                                              
    """)
else:
    print("Stone Port Scanner")
print("Ver : "+ver)
print('-' * 35)

if ports_file_bool and os.path.exists(ports_file_name):
    ports = []
    with open(ports_file_name) as f:
        ports.append(f.read().splitlines())
    print("PORTS : " + ports_file_name)
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
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.settimeout(0.5)  
    try:
        connection = s.connect((target, port))
        if not arr == True:
            print(str(target) + " : " + str(port))
        else:
            open_ports.append(str(target) + " : " + str(port))
        connection.close()
    except:
        pass
    
def scan_host(target):
    for element in ports[0]:
        portscan(int(element))
        #t.start()
    print(target + " STOP SCANNING")
    
def scan_host_multi(target):
    print(target + " START SCANNING")
    for element in ports[0]:
        t = threading.Thread(target=portscan, kwargs={'port': int(element), 'arr': True}) 
        t.start()
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
        scan_host_multi(target)
else:
    scan_host_multi(target)

input("\nPress enter...")
