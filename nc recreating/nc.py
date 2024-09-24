import argparse
import socket
import threading
import subprocess

def send_data(sock):
    try:
        while True:
            message = input() 
            sock.send(message.encode()) 
    except KeyboardInterrupt:
        sock.close()

def receive_data(sock):
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
    except KeyboardInterrupt:
        sock.close()

def execute_command(sock, command):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        while True:
            output = process.stdout.read(1024)
            if not output:
                break
            sock.send(output)
    except Exception as e:
        sock.send(str(e).encode())

def tcp_server(host, port, command=None):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f'Listening on {host}:{port}')

    conn, addr = server_socket.accept()
    print(f'Connection from {addr}')

    if command:
        execute_command(conn, command)
    else:
        receive_thread = threading.Thread(target=receive_data, args=(conn,))
        send_thread = threading.Thread(target=send_data, args=(conn,))
        receive_thread.start()
        send_thread.start()

def tcp_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f'Connected to {host}:{port}')

    receive_thread = threading.Thread(target=receive_data, args=(client_socket,))
    send_thread = threading.Thread(target=send_data, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

def udp_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    print(f'Listening on {host}:{port}')

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f'Received from {addr}: {data.decode()}')
        server_socket.sendto(b'Message received', addr)

def udp_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f'Sending data to {host}:{port}')

    while True:
        message = input()
        client_socket.sendto(message.encode(), (host, port))
        data, _ = client_socket.recvfrom(1024)
        print(f'Server response: {data.decode()}')

def main():
    parser = argparse.ArgumentParser(description="Netcat clone in Python with optional command execution")
    parser.add_argument('-l', '--listen', action='store_true', help="Listen mode, for incoming connections")
    parser.add_argument('-u', '--udp', action='store_true', help="Use UDP instead of TCP")
    parser.add_argument('-p', '--port', type=int, required=True, help="Port number to connect or bind to")
    parser.add_argument('-e', '--execute', help="Execute a command when a connection is received (server mode only)")
    parser.add_argument('host', nargs='?', default='127.0.0.1', help="Host to connect to or bind to (default: 127.0.0.1)")

    args = parser.parse_args()

    host = args.host
    port = args.port
    command = args.execute

    if args.listen:
        if args.udp:
            udp_server(host, port)
        else:
            tcp_server(host, port, command)
    else:
        if args.udp:
            udp_client(host, port)
        else:
            tcp_client(host, port)

if __name__ == "__main__":
    main()
