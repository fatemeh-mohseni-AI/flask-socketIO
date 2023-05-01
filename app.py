from flask import Flask, render_template
from flask_socketio import SocketIO
import os , subprocess

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('restart')
def handle_restart():
    os.system('touch restart')  # For Windows
    print("restart")
    # os.system('reboot')  # For Linux

@socketio.on('shutdown')
def handle_shutdown():
    os.system('touch shutdown')  # For Windows
    print("shutdown")
    # os.system('poweroff')  # For Linux

@socketio.on('user_input')
def handle_user_input(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        socketio.emit('output', output.decode())
    except subprocess.CalledProcessError as e:
        socketio.emit('error', e.output.decode())

        
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000)
