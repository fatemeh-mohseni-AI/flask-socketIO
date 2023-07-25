from server import socketio, app
import os
import yaml

config_ = os.path.join(os.getcwd(), "config")
config_address = os.path.join(config_, "config.yaml")
with open(config_address, 'r') as file:
    VALUE = yaml.safe_load(file)
    # check whether local or server is active
    for machine in VALUE:
        if VALUE[machine]["active"]:
            ip = VALUE[machine]['ip']
            port = int(VALUE[machine]['port'])
            break

if __name__ == "__main__":
    socketio.run(app, host=ip, port=int(port))
