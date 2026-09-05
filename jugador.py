import mysql.connector
import tabulate

import connector, equipo, estilos, validaciones

# Operaciones CRUD para la tabla jugadores

# Roles disponibles: el rol ya no se escribe libremente, se elige
# de esta lista para que no existan roles mal escritos o distintos
# entre si (ej. "Soporte" vs "soporte" vs "Suport").
ROLES_DISPONIBLES = [
    "Capitan",
    "Entrada",
    "Francotirador",
    "Soporte",
    "Estratega",
    "Suplente",
]


def registrar_jugador():
    estilos.titulo("REGISTRAR NUEVO JUGADOR", estilos.COLOR_JUGADOR)
    equipo.listar_equipos()
    estilos.aviso("\nEscribe 'volver' en cualquier campo para cancelar y regresar al menu.\n")

    nickname = validaciones.validar_texto("Nickname del jugador (unico): ", longitud_maxima=30)
    if nickname is None:
        estilos.aviso("Operacion cancelada.")
        return

    if existe_jugador(nickname):
        estilos.error(f"\n[ERROR] Ya existe un jugador con el nickname '{nickname}'. El nickname debe ser unico.")
        return

    nombre_real = validaciones.validar_texto("Nombre real: ", longitud_maxima=50, solo_letras=True)
    if nombre_real is None:
        estilos.aviso("Operacion cancelada.")
        return

    rol = validaciones.seleccionar_opcion("Selecciona el rol del jugador dentro del juego:", ROLES_DISPONIBLES)
    if rol is None:
        estilos.aviso("Operacion cancelada.")
        return

    codigo_equipo = validaciones.validar_texto("Codigo del equipo al que pertenece (ver tabla arriba): ")
    if codigo_equipo is None:
        estilos.aviso("Operacion cancelada.")
        return
    codigo_equipo = codigo_equipo.upper()

    if not equipo.existe_equipo(codigo_equipo):
        estilos.error(f"\n[ERROR] No existe ningun equipo con el codigo '{codigo_equipo}'. Registra primero el equipo.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = "INSERT INTO jugadores (nickname, nombre_real, rol, fk_codigo_equipo) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (nickname, nombre_real, rol, codigo_equipo))
        conexion.commit()
        estilos.exito(f"\nJugador '{nickname}' registrado correctamente.")
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo registrar el jugador: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al registrar el jugador: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def listar_jugadores():
    estilos.titulo("LISTADO DE JUGADORES", estilos.COLOR_JUGADOR)
    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT j.nickname, j.nombre_real, j.rol, e.nombre_equipo
            FROM jugadores j
            INNER JOIN equipo e ON j.fk_codigo_equipo = e.codigo_equipo
            ORDER BY e.nombre_equipo, j.nickname
        """
        cursor.execute(consulta)
        jugadores = cursor.fetchall()
        if not jugadores:
            estilos.aviso("No hay jugadores registrados.")
            return
        encabezados = ["Nickname", "Nombre real", "Rol", "Equipo"]
        tabla = tabulate.tabulate(jugadores, headers=encabezados, tablefmt="fancy_grid")
        estilos.imprimir_tabla(tabla, estilos.COLOR_JUGADOR)
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo listar los jugadores: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al listar los jugadores: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def actualizar_jugador():
    estilos.titulo("ACTUALIZAR JUGADOR", estilos.COLOR_JUGADOR)
    listar_jugadores()
    estilos.aviso("\nEscribe el nickname del jugador que quieres actualizar (o 'volver' para cancelar).\n")

    nickname = validaciones.validar_texto("Nickname del jugador a actualizar: ")
    if nickname is None:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM jugadores WHERE nickname = %s", (nickname,))
        jugador_encontrado = cursor.fetchone()
        if jugador_encontrado is None:
            estilos.aviso("No existe ningun jugador con ese nickname.")
            return

        nuevo_nombre = validaciones.validar_texto("Nuevo nombre real: ", longitud_maxima=50, solo_letras=True)
        if nuevo_nombre is None:
            estilos.aviso("Operacion cancelada.")
            return

        nuevo_rol = validaciones.seleccionar_opcion("Selecciona el nuevo rol del jugador:", ROLES_DISPONIBLES)
        if nuevo_rol is None:
            estilos.aviso("Operacion cancelada.")
            return

        equipo.listar_equipos()
        nuevo_codigo_equipo = validaciones.validar_texto("Nuevo codigo de equipo (ver tabla arriba): ")
        if nuevo_codigo_equipo is None:
            estilos.aviso("Operacion cancelada.")
            return
        nuevo_codigo_equipo = nuevo_codigo_equipo.upper()

        if not equipo.existe_equipo(nuevo_codigo_equipo):
            estilos.error(f"\n[ERROR] No existe ningun equipo con el codigo '{nuevo_codigo_equipo}'.")
            return

        consulta = "UPDATE jugadores SET nombre_real = %s, rol = %s, fk_codigo_equipo = %s WHERE nickname = %s"
        cursor.execute(consulta, (nuevo_nombre, nuevo_rol, nuevo_codigo_equipo, nickname))
        conexion.commit()
        estilos.exito("\nJugador actualizado correctamente.")
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo actualizar el jugador: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al actualizar el jugador: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def eliminar_jugador():
    estilos.titulo("ELIMINAR JUGADOR", estilos.COLOR_JUGADOR)
    listar_jugadores()
    estilos.aviso("\nEscribe el nickname del jugador que quieres eliminar (o 'volver' para cancelar).\n")

    nickname = validaciones.validar_texto("Nickname del jugador a eliminar: ")
    if nickname is None:
        estilos.aviso("Operacion cancelada.")
        return

    confirmacion = validaciones.confirmar_accion(f"¿Seguro que deseas eliminar al jugador '{nickname}'?")
    if not confirmacion:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM jugadores WHERE nickname = %s", (nickname,))
        conexion.commit()
        if cursor.rowcount == 0:
            estilos.aviso("No existe ningun jugador con ese nickname.")
        else:
            estilos.exito("\nJugador eliminado correctamente.")
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo eliminar el jugador: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al eliminar el jugador: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def existe_jugador(nickname):
    # <-- funcion de apoyo para validar unicidad antes de insertar
    conexion = connector.conectar()
    if conexion is None:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT nickname FROM jugadores WHERE nickname = %s", (nickname,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo verificar el jugador: {error}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
