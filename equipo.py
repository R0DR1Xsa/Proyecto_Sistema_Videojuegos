import mysql.connector
import tabulate

import connector, estilos, validaciones

# Operaciones CRUD para la tabla equipo


def registrar_equipo():
    estilos.titulo("REGISTRAR NUEVO EQUIPO", estilos.COLOR_EQUIPO)
    estilos.aviso("Escribe 'volver' en cualquier campo para cancelar y regresar al menu.\n")

    codigo = validaciones.validar_codigo_equipo("Codigo del equipo, formato EQ01 (unico): ")
    if codigo is None:
        estilos.aviso("Operacion cancelada.")
        return

    if existe_equipo(codigo):
        estilos.error(f"\n[ERROR] Ya existe un equipo con el codigo '{codigo}'. El codigo debe ser unico.")
        return

    nombre = validaciones.validar_texto("Nombre del equipo: ", longitud_maxima=50)
    if nombre is None:
        estilos.aviso("Operacion cancelada.")
        return

    pais = validaciones.validar_texto("Pais de procedencia: ", longitud_maxima=50, solo_letras=True)
    if pais is None:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        consulta = "INSERT INTO equipo (codigo_equipo, nombre_equipo, pais_procedencia) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (codigo, nombre, pais))
        conexion.commit()
        estilos.exito(f"\nEquipo '{nombre}' registrado correctamente.")
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo registrar el equipo: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al registrar el equipo: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def listar_equipos():
    estilos.titulo("LISTADO DE EQUIPOS", estilos.COLOR_EQUIPO)
    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_equipo, nombre_equipo, pais_procedencia FROM equipo ORDER BY codigo_equipo")
        equipos = cursor.fetchall()
        if not equipos:
            estilos.aviso("No hay equipos registrados.")
            return
        encabezados = ["Codigo", "Nombre", "Pais"]
        tabla = tabulate.tabulate(equipos, headers=encabezados, tablefmt="fancy_grid")
        estilos.imprimir_tabla(tabla, estilos.COLOR_EQUIPO)
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo listar los equipos: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al listar los equipos: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def actualizar_equipo():
    estilos.titulo("ACTUALIZAR EQUIPO", estilos.COLOR_EQUIPO)
    listar_equipos()
    estilos.aviso("\nEscribe el codigo del equipo que quieres actualizar (o 'volver' para cancelar).\n")

    codigo = validaciones.validar_texto("Codigo del equipo a actualizar: ")
    if codigo is None:
        estilos.aviso("Operacion cancelada.")
        return
    codigo = codigo.upper()

    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM equipo WHERE codigo_equipo = %s", (codigo,))
        equipo_encontrado = cursor.fetchone()
        if equipo_encontrado is None:
            estilos.aviso("No existe ningun equipo con ese codigo.")
            return

        nuevo_nombre = validaciones.validar_texto("Nuevo nombre del equipo: ", longitud_maxima=50)
        if nuevo_nombre is None:
            estilos.aviso("Operacion cancelada.")
            return

        nuevo_pais = validaciones.validar_texto("Nuevo pais de procedencia: ", longitud_maxima=50, solo_letras=True)
        if nuevo_pais is None:
            estilos.aviso("Operacion cancelada.")
            return

        consulta = "UPDATE equipo SET nombre_equipo = %s, pais_procedencia = %s WHERE codigo_equipo = %s"
        cursor.execute(consulta, (nuevo_nombre, nuevo_pais, codigo))
        conexion.commit()
        estilos.exito("\nEquipo actualizado correctamente.")
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo actualizar el equipo: {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al actualizar el equipo: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def eliminar_equipo():
    estilos.titulo("ELIMINAR EQUIPO", estilos.COLOR_EQUIPO)
    listar_equipos()
    estilos.aviso("\nEscribe el codigo del equipo que quieres eliminar (o 'volver' para cancelar).\n")

    codigo = validaciones.validar_texto("Codigo del equipo a eliminar: ")
    if codigo is None:
        estilos.aviso("Operacion cancelada.")
        return
    codigo = codigo.upper()

    confirmacion = validaciones.confirmar_accion(f"¿Seguro que deseas eliminar el equipo '{codigo}'?")
    if not confirmacion:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM equipo WHERE codigo_equipo = %s", (codigo,))
        conexion.commit()
        if cursor.rowcount == 0:
            estilos.aviso("No existe ningun equipo con ese codigo.")
        else:
            estilos.exito("\nEquipo eliminado correctamente.")
    except mysql.connector.Error as error:
        # <-- se dispara si el equipo tiene jugadores o partidos asociados (llave foranea)
        estilos.error(f"\n[ERROR] No se pudo eliminar el equipo (puede tener jugadores o partidos asociados): {error}")
    except Exception as error:
        estilos.error(f"\n[ERROR] Ocurrio un error inesperado al eliminar el equipo: {error}")
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()


def existe_equipo(codigo):
    # <-- funcion de apoyo usada por jugador.py y partido.py para validar antes de insertar
    conexion = connector.conectar()
    if conexion is None:
        return False
    cursor = None
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_equipo FROM equipo WHERE codigo_equipo = %s", (codigo,))
        return cursor.fetchone() is not None
    except mysql.connector.Error as error:
        estilos.error(f"\n[ERROR] No se pudo verificar el equipo: {error}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conexion.close()
