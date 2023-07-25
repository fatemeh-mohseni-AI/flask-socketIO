import socketio
import subprocess
import yaml

sio = socketio.Client()


@sio.event
def connect():
    print('Connected to server')


@sio.event
def message(data):
    print('Received message from server: ' + data)
    try:
        output = subprocess.check_output(data, shell=True, stderr=subprocess.STDOUT)
        sio.emit('output', output.decode())
    except subprocess.CalledProcessError as e:
        sio.emit('error', e.output.decode())


@sio.event
def status(data):
    print('Received message from server: ' + data)
    try:
        output = subprocess.check_output(data, shell=True, stderr=subprocess.STDOUT)
        sio.emit('service_out', output.decode())
    except subprocess.CalledProcessError as e:
        sio.emit('service_error', e.output.decode())


if __name__ == '__main__':
    with open('config/config.yaml', 'r') as file:
        VALUE = yaml.safe_load(file)
        ip = VALUE["SERVER"]['ip']
        port = int(VALUE["SERVER"]['port_client'])
    sio.connect(f"http://{ip}:{port}", wait_timeout=10)
    sio.wait()
