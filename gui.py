import asyncio
import tkinter as tk
from tkinter import ttk
import pickle
import subprocess
from getmac import get_mac_address as gma
import socket
import paramiko


def ButtonCallBack():
    mac = gma()
    os_ = os.get()
    pr_ = pr.get()

    app.destroy()
    json_data = {
        "os": f"{os_}",
        "mac": f"{mac}",
        "processor": f"{pr_}"
    }
    host = "172.20.10.5"
    print("HOST:", host)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username="root", password="root")
    transport = ssh.get_transport()
    dest_addr = ('127.0.0.1', 5000)
    local_forward_socket = transport.open_channel("direct-tcpip", (dest_addr), ('127.0.0.1', 5005))

    local_forward_socket.sendall(pickle.dumps(json_data))

    data = local_forward_socket.recv(1024).decode("utf-8")
    print('Received from server: ' + data)

    base_ip = host
    print(f"ssh -J root@{base_ip} root@{data}")

    subprocess.Popen(f"ssh -J root@{base_ip} root@{data}", shell=True).communicate()

    local_forward_socket.close()
    ssh.close()


app = tk.Tk()
app.geometry('240x150')

labelTop = tk.Label(app, text="Выберите операционную систему: ", width=0)
labelTop.grid(column=0, row=0, sticky="w", padx=4)

os_type = ["Alt Linix", "Ubuntu", "FreeBsd"]
os = ttk.Combobox(app, values=os_type, state="readonly", width=7)
os.grid(column=0, row=1, sticky="w", padx=4)
os.current(0)

processor_type = ["Intel", "Amd"]
pr = ttk.Combobox(app, values=processor_type, state="readonly", width=7)
pr.grid(column=0, row=3, sticky="w", padx=4)
pr.current(0)

processor_type_label = tk.Label(app, text="Выберите тип процессора: ")
processor_type_label.grid(column=0, row=2, sticky="w", padx=4)

bt = ttk.Button(app, text="OK", width=7, command=ButtonCallBack)
bt.grid(column=0, row=4, sticky="w", padx=4)
app.mainloop()
