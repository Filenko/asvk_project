import os.path
from os import listdir
import json
import pickle
from datetime import datetime
import logging
import subprocess
import sys
import time

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s]: %(message)s',
    handlers=[logging.StreamHandler()]
)

MACHINE_IS_UNREACHABLE_MESSAGE = "Machine is unreachable."


def ping(host):
    try:
        ping_output = subprocess.check_output(["ping", "-c", "1", "-W", "1", host])
        ping_time = float(ping_output.decode().split("time=")[1].split(" ms")[0])
        return ping_time
    except subprocess.CalledProcessError:
        return None


def machines_find(machines, ip):
    for machine in machines:
        if machine["ip"] == ip:
            return True
    return False


def GetAllMachines(folder):
    machinesInfo = listdir(folder)
    return machinesInfo


def LoadHistory(path):
    history = {}
    if os.path.exists(path):
        with open(path, "rb") as f:
            history = pickle.load(f)
            logging.debug(f'History loaded from: {path}')
    else:
        logging.debug(f'No history file at: {path}')
    return history


def SaveHistory(history, path):
    with open(path, "wb") as file:
        pickle.dump(history, file)


def LoadConfig(path="config.json"):
    loadedConfig = {}
    if os.path.exists(path):
        with open(path, 'r') as file:
            loadedConfig = json.load(file)
    else:
        logging.debug(f'No config file at: {path}')
    return loadedConfig


def GetCurrentMachines():
    allMachines = GetAllMachines("./machines")
    machines = []
    for machine_info in allMachines:
        with open(f"./machines/{machine_info}", "rb") as input_file:
            machineInfo = pickle.load(input_file)
            now = datetime.now()

            machineTimeStamp = os.stat(f"./machines/{machine_info}").st_mtime
            machineTime = datetime.fromtimestamp(machineTimeStamp)

            hour = machineTime.hour
            minute = machineTime.minute
            logging.debug(f'Machine with IP {machineInfo["ip"]} sent last info at {machineInfo["time"]}')
            if now.hour == hour and now.minute == minute:
                machines.append(machineInfo)
    logging.debug(f"It's {len(machines)} machines are ready now")
    return machines


def ChooseMachine(data):
    hist = LoadHistory("./history.pickle")
    machines = GetCurrentMachines()
    logging.debug("Loaded current machines!")
    machines.sort(key=lambda x: int(x["load_5"]))

    if data["fingerprint"] in hist:
        if machines_find(machines, hist[data["fingerprint"]]):
            pingTime = ping(hist[data['fingerprint']])
            if pingTime is not None:
                logging.debug(f"Connect this user to {hist[data['fingerprint']]} with ping {pingTime}. He was already connected to this machine.")
                return hist[data['fingerprint']]
            else:
                logging.debug(f"User was connected to {hist[data['fingerprint']]}. But this machine is unavailable now.")
        else:
            logging.debug(f"User was connected to {hist[data['fingerprint']]}. But this machine is unavailable now.")
    for i in range(len(machines)):
        logging.debug(f"Checking machine {i}")
        pingTime = ping(machines[i]["ip"])
        if pingTime is not None:
            logging.debug(f"Machine {i} is ready with ping {pingTime}. Return it.")
            hist[data["fingerprint"]] = machines[i]["ip"]
            SaveHistory(hist, "history.pickle")
            return machines[i]["ip"]
        logging.debug(f"Machine {i} is unreachable!")
    return None


def readServersFingerPrints(path='servers'):
    servers = set()
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f.readlines():
                servers.add(line.strip())
    else:
        logging.debug(f"No servers file at {path}")

    return servers

def ServerProgram(args):

    serversFingerPrints = readServersFingerPrints()

    if os.getenv('SSH_KEY_FINGERPRINT') in serversFingerPrints:
        serverParameters = json.loads(args[1])
        serverParameters["time"] = datetime.now()
        serverParameters["ip"] = os.getenv('SSH_CONNECTION').split()[0]
        with open(f'./machines/machine{serverParameters["machine_number"]}.pickle', 'wb') as f:
            pickle.dump(serverParameters, f)
        return

    giveAddress = False
    if len(args) >= 2 and args[1] == "giveAddress":
        giveAddress = True

    data = {}
    data["ip"] = os.getenv('SSH_CONNECTION').split()[0]
    data["fingerprint"] = os.getenv('SSH_KEY_FINGERPRINT')

    chosenMachineIp = ChooseMachine(data)
    logging.debug(f"Chose machine function returned: {chosenMachineIp}")
    if len(args) < 2:
        logging.info("Invalid arguments")
    name = args[1]
    if giveAddress:
        logging.info(f"{chosenMachineIp}")
    elif chosenMachineIp is not None:
        subprocess.Popen([f'ssh', f'{name}@{chosenMachineIp}']).communicate()


if __name__ == '__main__':
    ServerProgram(sys.argv)



