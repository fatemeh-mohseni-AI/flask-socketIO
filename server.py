from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import yaml
import os


config_ = os.path.join(os.getcwd(), "config")
config_address = os.path.join(config_, "config.yaml")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfagkja#asdgasdgasdg234F#$WFWf$%DFS!'
socketio = SocketIO(app, cors_allowed_origins='*')
connected_clients = []

with open(config_address, 'r') as file:
    VALUE = yaml.safe_load(file)
    password = VALUE["JETSON"]["password"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/clients')
def clients():
    return render_template('clients.html', clients=connected_clients)


@app.route('/service')
def services():
    return render_template('service.html')


@socketio.on('message')
def handle_message(message):
    """
    send any message come from web to all clients
    """

    print('received message from web: ' + message)
    emit("response", f'SERVER : I got message from web ---> {message}')   # send response to sender
    socketio.emit("message", message)  # send message to all clients


@socketio.on('output')
def handle_output(output):
    socketio.emit('response', F"RESULT : {output}")


@socketio.on('error')
def handle_error(error):
    socketio.emit('error', error)


# count connections

@socketio.on('connect')
def handle_connect():
    print('Client connected: ' + request.remote_addr)
    connected_clients.append(request.remote_addr)


@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected: ' + request.remote_addr)
    connected_clients.remove(request.remote_addr)


@socketio.on('kill_main')
def send_kill_main():
    """
    kill main command will kill process of running main code
    """
    command = "pkill -9 -f main.py"
    socketio.emit("message", command)


@socketio.on('smain')
def send_smain():
    """
    smain command will start process of running main code
    """
    command = "python3 /mnt/sda1/MAIN/AI_Robot/main.py"
    socketio.emit("message", command)


@socketio.on('show_ip')
def send_show_ip():
    """
    show ip command will shows internal ip
    """
    command = "ifconfig | grep 192"
    socketio.emit("message", command)


@socketio.on('sadid_ai')
def service_sadidai():
    """
    service sadid_ai status
    """
    command = f"echo {password} | sudo service sadid_ai status"
    socketio.emit("status", command)


@socketio.on('sadid_rosboard')
def service_sadid_rosboard():
    """
    service sadid_rosboard status
    """
    command = f"echo {password} | sudo service sadid_rosboard status"
    socketio.emit("status", command)


# -----------------------------------------------------
@socketio.on('restart_sadid_ai')
def service_restart_sadidai():
    """
    service sadid_ai status
    """
    command = f"echo {password} | sudo -S service sadid_ai restart"
    socketio.emit("status", command)


@socketio.on('restart_sadid_rosboard')
def service_restart_sadid_rosboard():
    """
    service sadid_rosboard restart
    """
    command = f"echo {password} | sudo -S service sadid_rosboard restart"
    socketio.emit("status", command)


@socketio.on('service_out')
def service_output(output):
    socketio.emit('service_out', F"RESULT : {output}")


@socketio.on('service_error')
def service_error(output):
    socketio.emit('service_error', F"ERROR : {output}")


# run the file
if __name__ == '__main__':
    with open(config_address, 'r') as file:
        VALUE = yaml.safe_load(file)
        # check whether local or server is active
        for machine in VALUE:
            if VALUE[machine]["active"]:
                ip = VALUE[machine]['ip']
                port = int(VALUE[machine]['port'])
                break
    file.close()
    socketio.run(app, host=ip, port=int(port), debug=True)
