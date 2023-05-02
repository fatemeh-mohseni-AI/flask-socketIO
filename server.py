from flask import Flask, render_template ,request
from flask_socketio import SocketIO, emit 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfagkja#$%DFS!'
socketio = SocketIO(app ,cors_allowed_origins='*')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('received message from web: ' + message)
    emit("response",f'SERVER : I got message from web ---> {message}')   # send response to sender
    socketio.emit("message",message)  # send message to all clients

@socketio.on('output')
def handle_output(output):
    print('received output: ' + output)
    socketio.emit('response', "successfully run on jetson ")

@socketio.on('error')
def handle_error(error):
    print('received error: ' + error)
    socketio.emit('error', error)


# count connections 
connected_clients = []
@app.route('/clients')
def clients():
    return render_template('clients.html', clients=connected_clients)

@socketio.on('connect')
def handle_connect():
    print('Client connected: ' + request.remote_addr)
    connected_clients.append(request.remote_addr)

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected: ' + request.remote_addr)
    connected_clients.remove(request.remote_addr)


if __name__ == '__main__':
    socketio.run(app, host='185.8.174.133', port=5000)
