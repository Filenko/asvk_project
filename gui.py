import asyncio
import tkinter as tk
from tkinter import ttk
import pickle
import subprocess
from getmac import get_mac_address as gma
import socket

def ButtonCallBack():
    mac = gma()
    os_ = os.get()
    pr_ = pr.get()

    app.destroy()
    jj = {
        "os": f"{os_}",
        "mac": f"{mac}",
        "processor": f"{pr_}"
    }
    host = "192.168.1.125"
    print("HOST:", host)
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    client_socket.sendall(pickle.dumps(jj))  # send message

    data = client_socket.recv(1024).decode("utf-8")  # receive response
    print('Received from server: ' + data)  # show in terminal

    base_ip = host
    print(f"ssh -J root@{base_ip} root@{data}")

    subprocess.Popen(f"ssh -J root@{base_ip} root@{data}", shell=True).communicate()

    client_socket.close()  # close the connection


app = tk.Tk()
app.geometry('240x150')

labelTop = tk.Label(app,text="Выберите операционную систему: ", width=0)
labelTop.grid(column=0, row=0, sticky="w", padx=4)

os_type=["Alt Linix","Ubuntu","FreeBsd"]
os = ttk.Combobox(app,values = os_type, state="readonly", width=7)
os.grid(column=0, row=1, sticky="w", padx=4)
os.current(0)

processor_type = ["Intel", "Amd"]
pr = ttk.Combobox(app,values = processor_type, state="readonly", width=7)
pr.grid(column=0, row=3, sticky="w", padx=4)
pr.current(0)

processor_type_label = tk.Label(app,text="Выберите тип процессора: ")
processor_type_label.grid(column=0, row=2, sticky="w", padx=4)

bt = ttk.Button(app, text="OK", width=7, command=ButtonCallBack)
bt.grid(column=0, row=4, sticky="w", padx=4)
app.mainloop()





