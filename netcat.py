# Python NetCat: "TCP/IP Swiss Army Knife"
# Adapted and annotated from "Black Hat Python"

import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading
def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    # Using subprocess' check_output method to run command on local OS and return output.
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()

class NetCat:
    # Initializing object with CLI args and buffer.
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        # Creating socket object.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()
    
    def send(self):
        # Connect to target and port.
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:
            self.socket.send(self.buffer)
        
        # Try/catch block to enable KeyboardInterrupt.
        try:
            # Start loop to receive data from target, break at tx end.
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break
                # Print re: data, pause for input, and continue.
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()
    
    def listen(self):
        # Binds to target, port.
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        # Listens in loop.
        while True:
            client_socket, _ = self.socket.accept()
            # Passes connected socket to handle()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()
    
    def handle(self, client_socket):
        # Execute command
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        # Upload file
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break
            
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        # Command prompt
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'PyCat: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server killed {e}')
                    self.socket.close()
                    sys.exit()


# Main block.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        # Example usage called with --help.
        description='Python Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.100 -p 4444 -l -c # command shell
            netcat.py -t 192.168.1.100 -p 4444 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.100 -p 4444 -l -e=\"cat /etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.100 -p 135 # echo 'ABC' to port 135
            netcat.py -t 192.168.1.100 -p 4444 # connect to server
        '''))
    # Using ArgParser for CLI, args specify program behavior.
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    # Sending empty buffer for listener, else stdin.
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
    
    nc = NetCat(args, buffer.encode())
    nc.run()
    