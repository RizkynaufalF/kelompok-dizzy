import socket
import threading

HOST = input("Masukkan alamat IP server: ")  
PORT = 65432 

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                print("Koneksi terputus dari server.")
                break
            print(message)
        except:
            print("Koneksi terputus dari server.")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        print(f"Gagal terhubung ke server: {e}")
        exit(1)
    
    username = input("Masukkan nama Anda: ")
    s.sendall(username.encode('utf-8'))

    # Buat thread untuk menerima pesan dari server
    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

    while True:
        message = input()
        if message.lower() == 'keluar':
            s.sendall('keluar'.encode('utf-8'))
            break
        s.sendall(f"{username}: {message}".encode('utf-8'))
