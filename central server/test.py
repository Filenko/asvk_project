import json

config = {
    "port": 5006,
    "host": "192.168.1.125"
}


with open('config.json', 'w') as file:
    json.dump(config, file)