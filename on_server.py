import json
from datetime import datetime
import subprocess
import os

machine_number = 1

dct = {}
dct["machine"] = machine_number
proc = subprocess.run(["who"], stdout=subprocess.PIPE)
ssh_connectios = proc.stdout.decode("utf-8").count("pts")
dct["ssh_connections"] = ssh_connectios
load_avg = os.getloadavg()
dct["load_1"] = load_avg[0]
dct["load_5"] = load_avg[1]
dct["load_15"] = load_avg[2]
dct["machine_number"] = machine_number
print([f"ssh", "balance@10.10.10.1", "python3", "balance.py", f"'{json.dumps(dct)}'"])
subprocess.run([f"ssh", "balance@10.10.10.1", "python3", "balance.py", f"'{json.dumps(dct)}'"])




