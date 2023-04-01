# Инструкция по использованию системы.

## Установка на центральный сервер

- Создать пользователя balance и в нем:
  - Установить git, python3
  - Скопировать файл update.py в ~
  - Запустить update.py и ввести цифру 1
  - В ~ создать папку machines

## Установка на конечные сервера:


- Установить python3, git
- Скопировать файл update.py в ~
- Запустить update.py и ввести цифру 2

```python
subprocess.run(["scp", f"machine_{machine_number}.pickle", f"root@10.10.10.1:~/machines/machine_{machine_number}.pickle"])
```
В строке 39 (выше) поменять 10.10.10.1 на ip адрес центрального сервера

- В /etc/systemd/system добавить два файла:

my.timer:
```text
[Unit]
Requires=my.service

[Timer]
Unit = my.service
OnUnitActiveSec=10s
AccuracySec=1s
[Install]
WantedBy=timers.target
```
my.service:
```text
[Unit]
Wants=my.timer

[Service]
ExecStart=/usr/bin/python3 /root/on_server.py
```

- В ~/.bashrc добавить строчку:
```text
systemctl start my.timer
```
(Если используются виртуальные машины, можно добавить так же:
```shell
ip a add dev eth1 10.10.10.x/24
ip l set eth1 up
```
Для автоматической настройки адресов при включении виртуалки (вместо x на разных машинах разные числа))

- Перезагрузить сервер или выполнить
```shell
systemctl start my.timer
```

- Создать пользователя/пользователей, в которых будут входить клиенты

## Как использовать клиент:

```shell
ssh balance@<ip address> python3 balance.py <name>
```