from tabulate import tabulate
from connector import conectar
from validaciones import validar_texto, validar_entero, validar_fecha, validar_hora, confirmar_accion
from equipo import existe_equipo

# partido.py
# Operaciones CRUD para la tabla partido
# + Bonus: tabla de posiciones (partidos jugados, ganados, perdidos)

def registrar_partido():
    print("\n--- REGISTRAR NUEVO PARTIDO ---")
    codigo_local = validar_texto("Codigo del equipo local: ").upper()
    codigo_visitante = validar_texto("Codigo del equipo visitante: ").upper()

    if codigo_local == codigo_visitante:
        print("\n[ERROR] Un equipo no puede jugar contra si mismo.")
        return

    if not existe_equipo(codigo_local):
        print(f"\n[ERROR] No existe ningun equipo con el codigo '{codigo_local}'.")
        return
    if not existe_equipo(codigo_visitante):
        print(f"\n[ERROR] No existe ningun equipo con el codigo '{codigo_visitante}'.")
        return

    fecha = validar_fecha("Fecha del partido (AAAA-MM-DD): ")
    hora = validar_hora("Hora del partido (HH:MM): ")
    marcador_local = validar_entero("Marcador del equipo local: ", minimo=0)
    marcador_visitante = validar_entero("Marcador del equipo visitante: ", minimo=0)
    arbitro = validar_texto("Nombre del arbitro: ")
    sede = validar_texto("Nombre/ciudad de la sede: ")

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO partido
            (codigo_equipo_local, codigo_equipo_visitante, fecha, hora,
             marcador_local, marcador_visitante, arbitro, sede)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (codigo_local, codigo_visitante, fecha, hora,
                                   marcador_local, marcador_visitante, arbitro, sede))
        conexion.commit()
        print("\nPartido registrado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo registrar el partido: {error}")
    finally:
        cursor.close()
        conexion.close()


def listar_partidos():
    print("\n--- LISTADO DE PARTIDOS ---")
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT p.id_partido, el.nombre_equipo AS local, ev.nombre_equipo AS visitante,
                   p.marcador_local, p.marcador_visitante, p.fecha, p.hora, p.arbitro, p.sede
            FROM partido p
            INNER JOIN equipo el ON p.codigo_equipo_local = el.codigo_equipo
            INNER JOIN equipo ev ON p.codigo_equipo_visitante = ev.codigo_equipo
            ORDER BY p.fecha, p.hora
        """
        cursor.execute(consulta)
        partidos = cursor.fetchall()
        if not partidos:
            print("No hay partidos registrados.")
            return
        encabezados = ["ID", "Local", "Visitante", "Marc. Local", "Marc. Visit.", "Fecha", "Hora", "Arbitro", "Sede"]
        print(tabulate(partidos, headers=encabezados, tablefmt="grid"))
    except Exception as error:
        print(f"\n[ERROR] No se pudo listar los partidos: {error}")
    finally:
        cursor.close()
        conexion.close()


def actualizar_partido():
    print("\n--- ACTUALIZAR PARTIDO ---")
    id_partido = validar_entero("ID del partido a actualizar: ", minimo=1)

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM partido WHERE id_partido = %s", (id_partido,))
        partido = cursor.fetchone()
        if partido is None:
            print("No existe ningun partido con ese ID.")
            return

        marcador_local = validar_entero("Nuevo marcador del equipo local: ", minimo=0)
        marcador_visitante = validar_entero("Nuevo marcador del equipo visitante: ", minimo=0)
        arbitro = validar_texto("Nuevo nombre del arbitro: ")
        sede = validar_texto("Nueva sede: ")

        consulta = """
            UPDATE partido
            SET marcador_local = %s, marcador_visitante = %s, arbitro = %s, sede = %s
            WHERE id_partido = %s
        """
        cursor.execute(consulta, (marcador_local, marcador_visitante, arbitro, sede, id_partido))
        conexion.commit()
        print("\nPartido actualizado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo actualizar el partido: {error}")
    finally:
        cursor.close()
        conexion.close()


def eliminar_partido():
    print("\n--- ELIMINAR PARTIDO ---")
    id_partido = validar_entero("ID del partido a eliminar: ", minimo=1)

    if not confirmar_accion(f"¿Seguro que deseas eliminar el partido #{id_partido}?"):
        print("Operacion cancelada.")
        return

    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM partido WHERE id_partido = %s", (id_partido,))
        conexion.commit()
        if cursor.rowcount == 0:
            print("No existe ningun partido con ese ID.")
        else:
            print("\nPartido eliminado correctamente.")
    except Exception as error:
        print(f"\n[ERROR] No se pudo eliminar el partido: {error}")
    finally:
        cursor.close()
        conexion.close()


def tabla_posiciones():
    # <-- RETO OPCIONAL (BONUS): partidos jugados, ganados y perdidos por equipo
    print("\n--- TABLA DE POSICIONES (BONUS) ---")
    conexion = conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_equipo, nombre_equipo FROM equipo ORDER BY nombre_equipo")
        equipos = cursor.fetchall()
        if not equipos:
            print("No hay equipos registrados.")
            return

        tabla = []
        for codigo_equipo, nombre_equipo in equipos:
            cursor.execute("""
                SELECT marcador_local, marcador_visitante, codigo_equipo_local
                FROM partido
                WHERE codigo_equipo_local = %s OR codigo_equipo_visitante = %s
            """, (codigo_equipo, codigo_equipo))
            partidos = cursor.fetchall()

            jugados = len(partidos)
            ganados = 0
            perdidos = 0

            for marcador_local, marcador_visitante, codigo_local in partidos:
                es_local = (codigo_local == codigo_equipo)
                marcador_propio = marcador_local if es_local else marcador_visitante
                marcador_rival = marcador_visitante if es_local else marcador_local

                if marcador_propio > marcador_rival:
                    ganados += 1
                elif marcador_propio < marcador_rival:
                    perdidos += 1
                # si hay empate no suma ni a ganados ni a perdidos

            tabla.append([nombre_equipo, jugados, ganados, perdidos])

        # Ordenar por partidos ganados de mayor a menor
        tabla.sort(key=lambda fila: fila[2], reverse=True)

        encabezados = ["Equipo", "PJ", "PG", "PP"]
        print(tabulate(tabla, headers=encabezados, tablefmt="grid"))
    except Exception as error:
        print(f"\n[ERROR] No se pudo calcular la tabla de posiciones: {error}")
    finally:
        cursor.close()
        conexion.close()
