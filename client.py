import socket

def main():
    # --- Configuración del cliente ---
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5000))
    print("Conectado al servidor de chat.")

    try:
        while True:
            mensaje = input("Escribe un mensaje o 'éxito' para salir: ")
            if mensaje.lower() == "exito" or mensaje.lower() == "éxito":
                break
            client_socket.sendall(mensaje.encode('utf-8'))
            respuesta = client_socket.recv(1024)
            print("Servidor:", respuesta.decode('utf-8'))
    except Exception as e:
        print(f"Error en el cliente: {e}")
    finally:
        client_socket.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    main()
