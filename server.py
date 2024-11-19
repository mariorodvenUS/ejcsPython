import socket
import threading
from termcolor import colored


# Función que maneja la conexión con cada cliente
def handle_client(client_socket, address):
    try:
        # Pedir el nombre de usuario al cliente
        client_socket.sendall(b"Introduce tu nombre de usuario: ")
        username = client_socket.recv(1024).decode('utf-8').strip()

        print(colored(f"[+] {username} se ha conectado desde {address}", "green"))

        while True:
            # Recibe mensajes del cliente
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8').strip()
            print(colored(f"[{username} - {address}] {message}", "blue"))
            # Envía el mismo dato de vuelta al cliente, incluyendo el nombre de usuario
            client_socket.sendall(f"{username}: {message}".encode('utf-8'))
    except ConnectionResetError:
        print(colored(f"[-] Conexión cerrada por el cliente {address}", "red"))
    finally:
        client_socket.close()


# Función que crea un servidor en un puerto específico
def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(colored(f"[+] Servidor escuchando en el puerto {port}", "green"))

    while True:
        client_socket, address = server.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket, address))
        client_handler.start()


# Crear servidores en los puertos 9000-9009
for port in range(9000, 9010):
    server_thread = threading.Thread(target=start_server, args=(port,))
    server_thread.start()
