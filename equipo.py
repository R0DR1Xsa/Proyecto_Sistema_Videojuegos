from tabulate import tabulate
from connector import conectar
from validaciones import validar_texto, confirmar_accion

# equipo.py
# Operaciones CRUD para la tabla equipo

def registrar_equipo():
    print("\n--- REGISTRAR NUEVO EQUIPO ---")
    codigo = validar_texto("Codigo del equipo (unico): ").upper()
    nombre = validar_texto("Nombre del equipo: ")
    pais = validar_texto("Pais de procedencia: ")

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = "INSERT INTO equipo (codigo_equipo, nombre_equipo, pais_procedencia) VALUES (%s, %s, %s)"
        cursor.execute(consulta, (codigo, nombre, pais))
        conexion.commit()
        print(f"\nEquipo '{nombre}' registrado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo registrar el equipo: {error}")
    finally:
        cursor.close()
        conexion.close()


def listar_equipos():
    print("\n--- LISTADO DE EQUIPOS ---")
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_equipo, nombre_equipo, pais_procedencia FROM equipo ORDER BY codigo_equipo")
        equipos = cursor.fetchall()
        if not equipos:
            print("No hay equipos registrados.")
            return
        encabezados = ["Codigo", "Nombre", "Pais"]
        print(tabulate(equipos, headers=encabezados, tablefmt="grid"))
    except Exception as error:
        print(f"\n[ERROR] No se pudo listar los equipos: {error}")
    finally:
        cursor.close()
        conexion.close()


def actualizar_equipo():
    print("\n--- ACTUALIZAR EQUIPO ---")
    codigo = validar_texto("Codigo del equipo a actualizar: ").upper()

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM equipo WHERE codigo_equipo = %s", (codigo,))
        equipo = cursor.fetchone()
        if equipo is None:
            print("No existe ningun equipo con ese codigo.")
            return

        nuevo_nombre = validar_texto("Nuevo nombre del equipo: ")
        nuevo_pais = validar_texto("Nuevo pais de procedencia: ")

        consulta = "UPDATE equipo SET nombre_equipo = %s, pais_procedencia = %s WHERE codigo_equipo = %s"
        cursor.execute(consulta, (nuevo_nombre, nuevo_pais, codigo))
        conexion.commit()
        print("\nEquipo actualizado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo actualizar el equipo: {error}")
    finally:
        cursor.close()
        conexion.close()


def eliminar_equipo():
    print("\n--- ELIMINAR EQUIPO ---")
    codigo = validar_texto("Codigo del equipo a eliminar: ").upper()

    if not confirmar_accion(f"¿Seguro que deseas eliminar el equipo '{codigo}'?"):
        print("Operacion cancelada.")
        return

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM equipo WHERE codigo_equipo = %s", (codigo,))
        conexion.commit()
        if cursor.rowcount == 0:
            print("No existe ningun equipo con ese codigo.")
        else:
            print("\nEquipo eliminado correctamente.")
    except Exception as error:
        # <-- se dispara si el equipo tiene jugadores o partidos asociados (llave foranea)
        print(f"\n[ERROR] No se pudo eliminar el equipo (puede tener jugadores o partidos asociados): {error}")
    finally:
        cursor.close()
        conexion.close()


def existe_equipo(codigo):
    # <-- funcion de apoyo usada por jugador.py y partido.py para validar antes de insertar
    conexion = conectar()
    if conexion is None:
        return False
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_equipo FROM equipo WHERE codigo_equipo = %s", (codigo,))
        return cursor.fetchone() is not None
    finally:
        cursor.close()
        conexion.close()
