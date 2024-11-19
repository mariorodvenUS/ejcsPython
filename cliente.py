import socket
from tqdm import tqdm
from termcolor import colored
import time

# Configuración del servidor

SERVER_IP=input(colored("[?]Introduce la ip a la que te quieres conectar:", "blue"))

# Pedir al usuario un puerto válido entre 9000 y 9009
while True:
    try:
        SERVER_PORT = int(input(colored("Introduce un puerto entre 9000 y 9009: ", "cyan")))
        if 9000 <= SERVER_PORT <= 9009:
            break
        else:
            print(colored("El puerto debe estar entre 9000 y 9009.", "red"))
    except ValueError:
        print(colored("Introduce un número válido.", "red"))


# Función para conectarse al servidor y manejar la comunicación
def connect_to_server():
    # Crear el socket del cliente
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mostrar una barra de progreso mientras se conecta
    with tqdm(total=100, desc="Conectando al servidor",
              bar_format="{l_bar}{bar} [Tiempo restante: {remaining}]") as pbar:
        for _ in range(10):
            time.sleep(0.1)  # Simula la conexión
            pbar.update(10)

    # Conectar al servidor
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print(colored("[+] Conexión establecida con el servidor", "green"))

    # Recibir la solicitud de nombre de usuario
    prompt = client_socket.recv(1024).decode('utf-8')
    print(colored(prompt, "cyan"))
    username = input(colored("Tu nombre de usuario: ", "yellow"))

    # Enviar el nombre de usuario al servidor
    client_socket.sendall(username.encode('utf-8'))

    # Comienza a enviar y recibir mensajes
    try:
        while True:
            # Leer el mensaje del usuario y enviarlo al servidor
            message = input(colored(f"{username} > ", "yellow"))
            client_socket.sendall(message.encode('utf-8'))

            # Recibir y mostrar la respuesta del servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(colored(response, "blue"))

    except KeyboardInterrupt:
        print(colored("\n[-] Conexión cerrada", "red"))

    finally:
        client_socket.close()


# Ejecuta el cliente
connect_to_server()
