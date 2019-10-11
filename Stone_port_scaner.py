#
#   STONE PORT SCAN
#  [ Stolar Studio ]
#

ver = "0.1.1"

import threading 
import socket
import os
import configparser

print("""
   _____ _                     _____           _      _____                           
  / ____| |                   |  __ \         | |    / ____|                          
 | (___ | |_ ___  _ __   ___  | |__) |__  _ __| |_  | (___   ___ __ _ _ __   ___ _ __ 
  \___ \| __/ _ \| '_ \ / _ \ |  ___/ _ \| '__| __|  \___ \ / __/ _` | '_ \ / _ \ '__|
  ____) | || (_) | | | |  __/ | |  | (_) | |  | |_   ____) | (_| (_| | | | |  __/ |   
 |_____/ \__\___/|_| |_|\___| |_|   \___/|_|   \__| |_____/ \___\__,_|_| |_|\___|_|                                                                                                                                                                            
""")
print("Ver : "+ver)
print('-' * 35)

if not os.path.exists("settings.txt"):
    config = configparser.ConfigParser()
    config.add_section("Settings")
    config.set("Settings", "hosts-file", "false")
    config.set("Settings", "hosts-file-name", "hosts.txt")
    config.set("Settings", "ports-file", "false")
    config.set("Settings", "ports-file-name", "ports.txt")
    with open("settings.txt", "w") as config_file:
        config.write(config_file)
try:
    config = configparser.ConfigParser()
    config.read("settings.txt")
    hosts_file = config.get("Settings", "hosts-file")
    hosts_file_name = config.get("Settings", "hosts-file-name")
    ports_file = config.get("Settings", "ports-file")
    ports_file_name = config.get("Settings", "ports-file-name")
    
    #ports_file = "false"
except:
    print("ERROR READ SETTINGS FILE")
    input("\nPress enter...")
    exit()

hosts_file_bool = True if hosts_file == 'true' or hosts_file == 'True' else False
ports_file_bool = True if ports_file == 'true' or ports_file == 'True' else False

if ports_file_bool and os.path.exists(ports_file_name):
    ports = []
    with open(ports_file_name) as f:
        ports.append(f.read().splitlines())
    print("PORTS : ", end = '')
    print(ports)
else:
    ports = [[21, 22, 23, 25, 38, 43 , 999, 109, 110, 115, 118, 119, 143,  
    194, 220, 443, 540, 585, 591, 1112, 1433, 1443, 3128, 3197,
    3306, 4000, 4333, 5100, 5432, 6669, 8000, 8080, 9014, 9200, 80]]

if hosts_file_bool and os.path.exists(hosts_file_name):
    hosts = []
    with open(hosts_file_name) as f:
        hosts.append(f.read().splitlines())
    print("HOSTS : ", end = '')
    print(hosts)
else:
    target = input('Enter host : ')
    
print('-' * 35)

#open_ports = []

def portscan(port):  
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    s.settimeout(0.5)  
    try:
        connection = s.connect((target, port))  
        #print('Port :', port, "is open.")
        #open_ports.append(str(target) + " : " + str(port))
        print(str(target) + " : " + str(port))
        connection.close()   
    except:
        pass   

if hosts_file_bool:
    for target in hosts[0]:
        for element in ports[0]:
            t = threading.Thread(target=portscan, kwargs={'port': int(element)}) 
            t.start()   
else:
    for element in ports[0]:
        t = threading.Thread(target=portscan, kwargs={'port': int(element)}) 
        t.start()
"""
if len(open_ports) > 0:
    print("OPENED PORTS : \n")
    for i in open_ports:
        print(i)
else:
    print("NO OPEN PORTS FOUND")
"""

input("\nPress enter...")
