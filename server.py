import socket
import threading
import sqlite3
from datetime import datetime

# --- Configuración de la base de datos ---
DB_FILE = 'chat.db'

def init_db():
    """Inicializa la base de datos y crea la tabla de mensajes si no existe."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conn.commit()

def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    """Guarda un mensaje en la base de datos."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        conn.commit()

# --- Configuración del socket TCP/IP ---
def inicializar_socket():
    """Inicializa el socket del servidor."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))  # Escuchar en localhost:5000
    server_socket.listen()
    print("Servidor escuchando en localhost:5000")
    return server_socket

def manejar_cliente(conn, addr):
    """Maneja la conexión de un cliente."""
    print(f"Conexión aceptada de {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensaje = data.decode('utf-8').strip()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            guardar_mensaje(mensaje, timestamp, addr[0])
            respuesta = f"Mensaje recibido: {timestamp}"
            conn.sendall(respuesta.encode('utf-8'))
    except Exception as e:
        print(f"Error manejando cliente {addr}: {e}")
    finally:
        conn.close()
        print(f"Conexión cerrada de {addr}")

def aceptar_conexiones(server_socket):
    """Acepta conexiones entrantes de clientes."""
    try:
        while True:
            conn, addr = server_socket.accept()
            threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True).start()
    except Exception as e:
        print(f"Error aceptando conexiones: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    try:
        init_db()
        server_socket = inicializar_socket()
        aceptar_conexiones(server_socket)
    except OSError as e:
        print(f"Error: {e}")
    except sqlite3.Error as e:
        print(f"Error de base de datos: {e}")
