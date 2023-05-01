# flask-socketIO
The Python file is a Flask web application that allows users to execute commands on the server and perform system operations like restart and shutdown. The application uses the Flask web framework and Flask-SocketIO library to create a real-time communication between the client and server.
The index() function returns a rendered HTML template that serves as the main page of the application. The handle_restart() and handle_shutdown() functions are SocketIO event handlers that are triggered when the client sends a "restart" or "shutdown" event, respectively. These functions execute system commands to restart or shutdown the server, depending on the operating system.
The handle_user_input() function is another SocketIO event handler that is triggered when the client sends a "user_input" event with a command string as the payload. This function uses the subprocess module to execute the command on the server and capture its output. The output is then sent back to the client using a "output" event, or an "error" event if the command execution fails.
The script also includes a check to ensure that it is being run as the main program and starts the SocketIO server on the specified host and port.
It is important to note that user input should be validated and sanitized to prevent malicious commands from being executed on the server. Additionally, user authentication and authorization should be implemented to ensure that only authorized users are allowed to execute commands on the server.

RUN:
python3 app.py
