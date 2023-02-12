from datetime import datetime
import pickle
import subprocess
import os
import socket
import fcntl
import struct

machine_number = 1

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])


now = datetime.now()
current_time = now.strftime("%H:%M:%S")
dct = {}
dct["time"] = current_time
dct["machine"] = machine_number
dct["ip"] = get_ip_address('eth1')
proc = subprocess.run(["who"], stdout=subprocess.PIPE)
ssh_connectios = proc.stdout.decode("utf-8").count("pts")
dct["ssh_connections"] = ssh_connectios
load_avg = os.getloadavg()
dct["load_1"] = load_avg[0]
dct["load_5"] = load_avg[1]
dct["load_15"] = load_avg[2]

for (key, value) in dct.items():
    print(key, value)

with open(f'machine_{machine_number}.pickle', 'wb') as handle:
    pickle.dump(dct, handle, protocol=pickle.HIGHEST_PROTOCOL)
subprocess.run(["scp", f"machine_{machine_number}.pickle", f"root@10.10.10.1:~/machines/machine_{machine_number}.pickle"])



