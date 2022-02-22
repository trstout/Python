import socket
import threading

IP = '0.0.0.0'
PORT = 9998

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP,PORT)) # pass IP & port we want server to listen on
    server.listen(5) # tell server to listen w/ max backlogged connections set to 5
    print(f'[*] Listening on {IP}:{PORT}')
    
    while True: # main loop for server
        client, address = server.accept() #client connects
        print(f'[*] Accepted connection from {address[0]}:{address[1]}')
        client_handler = threading.Thread(target=handle_client, args=(client,)) # client socket in 'client' variable and remote connection details in 'address' variable
        client_handler.start() # start thread to handle client connection

def handle_client(client_socket):
    with client_socket as sock:
        request = sock.recv(1024)
        print(f'[*] Received: {request.decode("utf-8")}')
        sock.send(b'ACK') # handle_client performs recv() and sends ACK to client.
        
if __name__ == '__main__':
    main()        