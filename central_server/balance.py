import os.path
from os import listdir
import json
import socket
import pickle
from datetime import datetime
import logging
import ping3
import subprocess
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s]: %(message)s',
    handlers=[logging.StreamHandler()]
)

MACHINE_IS_UNREACHABLE_MESSAGE = "Machine is unreachable."

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
    return history


def SaveHistory(history, path):
    with open(path, "wb") as file:
        pickle.dump(history, file)


def LoadConfig(path="config.json"):
    with open(path, 'r') as file:
        loadedConfig = json.load(file)
    return loadedConfig


def GetCurrentMachines():
    allMachines = GetAllMachines("./machines")
    machines = []
    for machine_info in allMachines:
        with open(f"./machines/{machine_info}", "rb") as input_file:
            machineInfo = pickle.load(input_file)
            now = datetime.now()
            hour = datetime.strptime(machineInfo["time"], "%H:%M:%S").hour
            minute = datetime.strptime(machineInfo["time"], "%H:%M:%S").minute
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

    if data["mac"] in hist:
        if machines_find(machines, hist[data["mac"]]):
            logging.info(f"Connect this user to {hist[data['mac']]}. He was already connected to this machine.")
            return hist[data['mac']]
        else:
            logging.info(f"User was connected to {hist[data['mac']]}. But this machine is unavailable now.")
    for i in range(len(machines)):
        logging.debug(f"Checking machine {i}")
        pingTime = ping3.ping(machines[i]["ip"], timeout=1)
        if pingTime is not None:
            logging.debug(f"Machine {i} is ready. Return it.")
            hist[data["mac"]] = machines[i]["ip"]
            SaveHistory(hist, "history.pickle")
            return machines[i]["ip"]
        logging.debug(f"Machine {i} is unreachable!")
    return None


def ServerProgram(config, args):

    result = subprocess.check_output("echo $SSH_CLIENT | awk '{print $1}'", shell=True)
    ip_address = result.decode().strip()
    print("ARGS", args)
    print("IP address:", ip_address)

    result = subprocess.check_output("arp -a $(echo $SSH_CLIENT | awk '{print $1}') | awk '{print $4}'", shell=True)
    mac_address = result.decode().strip()

    print("MAC address:", mac_address)
    # chosenMachineIp = ChooseMachine(data)
    # conn.send(chosenMachineIp.encode("utf-8"))
    #
    #     logging.info(f'Connect this user to {chosenMachineIp}')
    # except Exception as e:
    #     logging.error(str(e))
    #     server_socket.close()


if __name__ == '__main__':
    config = LoadConfig()
    ServerProgram(config, sys.argv)
