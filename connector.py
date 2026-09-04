import mysql.connector
from mysql.connector import Error

# Unico punto de conexion a la base de datos (gateway).
# Todos los demas modulos importan conectar() desde aqui.

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="140105",            # <-- coloca aqui tu contraseña de MySQL
            database="torneo_videojuegos"
        )
        return conexion
    except Error as error:
        print(f"\n[ERROR] No se pudo conectar a la base de datos: {error}\n")
        return None
