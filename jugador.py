from tabulate import tabulate
from connector import conectar
from validaciones import validar_texto, confirmar_accion
from equipo import existe_equipo

# jugador.py
# Operaciones CRUD para la tabla jugador

def registrar_jugador():
    print("\n--- REGISTRAR NUEVO JUGADOR ---")
    nickname = validar_texto("Nickname del jugador (unico): ")
    nombre_real = validar_texto("Nombre real: ")
    rol = validar_texto("Rol dentro del juego (ej: soporte, francotirador, capitan): ")
    codigo_equipo = validar_texto("Codigo del equipo al que pertenece: ").upper()

    if not existe_equipo(codigo_equipo):
        print(f"\n[ERROR] No existe ningun equipo con el codigo '{codigo_equipo}'. Registra primero el equipo.")
        return

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = "INSERT INTO jugador (nickname, nombre_real, rol, codigo_equipo) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (nickname, nombre_real, rol, codigo_equipo))
        conexion.commit()
        print(f"\nJugador '{nickname}' registrado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo registrar el jugador: {error}")
    finally:
        cursor.close()
        conexion.close()


def listar_jugadores():
    print("\n--- LISTADO DE JUGADORES ---")
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT j.nickname, j.nombre_real, j.rol, e.nombre_equipo
            FROM jugador j
            INNER JOIN equipo e ON j.codigo_equipo = e.codigo_equipo
            ORDER BY e.nombre_equipo, j.nickname
        """
        cursor.execute(consulta)
        jugadores = cursor.fetchall()
        if not jugadores:
            print("No hay jugadores registrados.")
            return
        encabezados = ["Nickname", "Nombre real", "Rol", "Equipo"]
        print(tabulate(jugadores, headers=encabezados, tablefmt="grid"))
    except Exception as error:
        print(f"\n[ERROR] No se pudo listar los jugadores: {error}")
    finally:
        cursor.close()
        conexion.close()


def actualizar_jugador():
    print("\n--- ACTUALIZAR JUGADOR ---")
    nickname = validar_texto("Nickname del jugador a actualizar: ")

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM jugador WHERE nickname = %s", (nickname,))
        jugador = cursor.fetchone()
        if jugador is None:
            print("No existe ningun jugador con ese nickname.")
            return

        nuevo_nombre = validar_texto("Nuevo nombre real: ")
        nuevo_rol = validar_texto("Nuevo rol: ")
        nuevo_codigo_equipo = validar_texto("Nuevo codigo de equipo: ").upper()

        if not existe_equipo(nuevo_codigo_equipo):
            print(f"\n[ERROR] No existe ningun equipo con el codigo '{nuevo_codigo_equipo}'.")
            return

        consulta = "UPDATE jugador SET nombre_real = %s, rol = %s, codigo_equipo = %s WHERE nickname = %s"
        cursor.execute(consulta, (nuevo_nombre, nuevo_rol, nuevo_codigo_equipo, nickname))
        conexion.commit()
        print("\nJugador actualizado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo actualizar el jugador: {error}")
    finally:
        cursor.close()
        conexion.close()


def eliminar_jugador():
    print("\n--- ELIMINAR JUGADOR ---")
    nickname = validar_texto("Nickname del jugador a eliminar: ")

    if not confirmar_accion(f"¿Seguro que deseas eliminar al jugador '{nickname}'?"):
        print("Operacion cancelada.")
        return

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM jugador WHERE nickname = %s", (nickname,))
        conexion.commit()
        if cursor.rowcount == 0:
            print("No existe ningun jugador con ese nickname.")
        else:
            print("\nJugador eliminado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo eliminar el jugador: {error}")
    finally:
        cursor.close()
        conexion.close()
