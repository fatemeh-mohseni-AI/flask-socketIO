from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'uj7JH98j8UFHE8QJ3489f@#$@#RSD5FWR5efaer35f!'
socketio = SocketIO(app)

def clientdata(datas):
    print("this is datas" , datas)
    if "shutdown" in str(datas):
        response = "sudo shutdown"

    elif "reboot" in str(datas):
        response = "sudo reboot"
   
    elif "test" in str(datas):
        response = "touch tst.txt"

    else:
        response = "message recieved and lead into taking no action"

    return response


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('user_input')
def handle_user_input(data):
    print('Received user input:', data)
    resp = clientdata(data)
    emit('response', resp)

if __name__ == '__main__':
    socketio.run(app, host="185.8.174.133", port=5000)
