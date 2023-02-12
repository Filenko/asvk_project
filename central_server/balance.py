from os import listdir
import json
import socket
import pickle
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    handlers=[logging.StreamHandler()]
)


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
    with open(path, "wb") as f:
        logging.debug('History loaded from: ', path)
        pickle.dump(history, f)
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
            if now.hour == hour and now.minute == minute:
                machines.append(machineInfo)
    logging.debug(f"It's {len(machines)} now")
    return machines


def ChooseMachine(data):
    hist = LoadHistory("./history.pickle")
    machines = GetCurrentMachines()
    machines.sort(key=lambda x: int(x["load_5"]))

    if data["mac"] in hist:
        if machines_find(machines, hist[data["mac"]]):
            logging.info(f"Connect this user to {hist[data['mac']]}. He was already connected to this machine.")
            return hist[data['mac']]
        else:
            logging.info(f"User was connected to {hist[data['mac']]}. But this machine is unavailable now.")

    hist[data["mac"]] = machines[0]["ip"]
    SaveHistory(hist, "history.pickle")
    return machines[0]["ip"]


def ServerProgram(config):
    host = config["host"]
    port = config["port"]
    print(host, port, sep="\n")
    logging.info('Host: ', host)
    logging.info('Port: ', port)

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)

    try:
        while True:
            conn, address = server_socket.accept()
            logging.info('Connection from: ', str(address))
            data = conn.recv(1024)
            if not data:
                continue
            else:
                data = pickle.loads(data)

            logging.info("Received from client: ", data)
            chosenMachineIp = ChooseMachine(data)
            conn.send(chosenMachineIp.encode("utf-8"))
            logging.info(f'Connect this user to {chosenMachineIp}')
    except:
        server_socket.close()


if __name__ == '__main__':
    config = LoadConfig()
    ServerProgram(config)
