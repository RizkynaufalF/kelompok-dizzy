import socket
import threading

HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:  # Don't send the message back to the sender
            try:
                client.sendall(message)
            except:
                client.close()
                clients.remove(client)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            broadcast(data, conn)  # Broadcast message to other clients
    finally:
        conn.close()
        clients.remove(conn)
        print(f"Disconnected from {addr}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is listening...")
    
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
