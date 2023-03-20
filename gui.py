import asyncio
import tkinter as tk
from tkinter import ttk
import pickle
import subprocess
from getmac import get_mac_address as gma
import socket
import paramiko


def create_popup(title, text):
    popup = tk.Toplevel(os)
    popup.title(title)
    popup.geometry("250x100")
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x = (screen_width - popup.winfo_reqwidth()) // 2
    y = (screen_height - popup.winfo_reqheight()) // 2
    popup.geometry("+{}+{}".format(x, y))
    label = tk.Label(popup, text=text)
    label.pack(pady=10)
    button = tk.Button(popup, text="Закрыть", command=popup.destroy)
    button.pack()
    return popup


def ButtonCallBack():
    mac = gma()
    os_ = os.get()
    pr_ = pr.get()

    json_data = {
        "os": f"{os_}",
        "mac": f"{mac}",
        "processor": f"{pr_}"
    }
    host = "10.10.10.10"
    print("HOST:", host)
    print(json_data)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username="root", password="root")
        transport = ssh.get_transport()
        dest_addr = ('127.0.0.1', 5000)
        local_forward_socket = transport.open_channel("direct-tcpip", (dest_addr), ('127.0.0.1', 5005))
        local_forward_socket.sendall(pickle.dumps(json_data))

        data = local_forward_socket.recv(1024).decode("utf-8")
        if data is None:
            create_popup("Ошибка", "Не нашлось подходящей машины. Попробуйте снова.")
        print('Received from server: ' + data)


        base_ip = host
        print(f"ssh -J root@{base_ip} root@{data}")

        subprocess.Popen(f"ssh -J root@{base_ip} root@{data}", shell=True).communicate()
        local_forward_socket.close()
        ssh.close()
    except:
        create_popup("Ошибка", 'Центральный сервер недоступен')
        return


# app = tk.Tk()
# app.geometry('240x150')
# app.eval('tk::PlaceWindow . center')
#
# labelTop = tk.Label(app, text="Выберите операционную систему: ", width=0)
# labelTop.grid(column=0, row=0, sticky="w", padx=4)
#
# os_type = ["Alt Linix", "Ubuntu", "FreeBsd"]
# os = ttk.Combobox(app, values=os_type, state="readonly", width=7)
# os.grid(column=0, row=1, sticky="w", padx=4)
# os.current(0)
#
# processor_type = ["Intel", "Amd"]
# pr = ttk.Combobox(app, values=processor_type, state="readonly", width=7)
# pr.grid(column=0, row=3, sticky="w", padx=4)
# pr.current(0)
#
# processor_type_label = tk.Label(app, text="Выберите тип процессора: ")
# processor_type_label.grid(column=0, row=2, sticky="w", padx=4)
#
# bt = ttk.Button(app, text="OK", width=7, command=ButtonCallBack)
# bt.grid(column=0, row=4, sticky="w", padx=4)
# app.mainloop()


app = tk.Tk()
app.geometry("250x200+{}+{}".format(int(app.winfo_screenwidth() / 2 - 150), int(app.winfo_screenheight() / 2 - 100)))
app.resizable(False, False)
app.title("Connection ")


osType = ["Alt Linux", "Ubuntu", "FreeBSD"]
os = ttk.Combobox(app, values=osType)
os.set("Choose os type: ")
os.pack(pady=5)

processor = ["Intel", "Amd"]
pr = ttk.Combobox(app, values=processor)
pr.set("Choose processor type: ")
pr.pack(pady=5)

ramType = ["4Gb", "8Gb", "16Gb"]
ram = ttk.Combobox(app, values = ramType)
ram.set("Choose ram: ")
ram.pack(pady=5)

checkbox = tk.Checkbutton(app, text="Reconnect?")
checkbox.pack(anchor=tk.W, padx=20, pady=5)

button = ttk.Button(app, text="Connect", command=ButtonCallBack)
button.pack(pady=5)



# Run the main loop
app.mainloop()



