import tabulate

import connector, equipo, estilos, validaciones

# Operaciones CRUD para la tabla partido
# + Bonus: tabla de posiciones (partidos jugados, ganados, perdidos)


def registrar_partido():
    estilos.titulo("REGISTRAR NUEVO PARTIDO", estilos.COLOR_PARTIDO)
    equipo.listar_equipos()
    estilos.aviso("\nEscribe 'volver' en cualquier campo para cancelar y regresar al menu.\n")

    codigo_local = validaciones.validar_texto("Codigo del equipo local (ver tabla arriba): ")
    if codigo_local is None:
        estilos.aviso("Operacion cancelada.")
        return
    codigo_local = codigo_local.upper()

    codigo_visitante = validaciones.validar_texto("Codigo del equipo visitante (ver tabla arriba): ")
    if codigo_visitante is None:
        estilos.aviso("Operacion cancelada.")
        return
    codigo_visitante = codigo_visitante.upper()

    if codigo_local == codigo_visitante:
        estilos.error("\n[ERROR] Un equipo no puede jugar contra si mismo.")
        return

    if not equipo.existe_equipo(codigo_local):
        estilos.error(f"\n[ERROR] No existe ningun equipo con el codigo '{codigo_local}'.")
        return
    if not equipo.existe_equipo(codigo_visitante):
        estilos.error(f"\n[ERROR] No existe ningun equipo con el codigo '{codigo_visitante}'.")
        return

    fecha = validaciones.validar_fecha("Fecha del partido (AAAA-MM-DD): ")
    if fecha is None:
        estilos.aviso("Operacion cancelada.")
        return

    hora = validaciones.validar_hora("Hora del partido (HH:MM): ")
    if hora is None:
        estilos.aviso("Operacion cancelada.")
        return

    marcador_local = validaciones.validar_entero("Marcador del equipo local: ", minimo=0)
    if marcador_local is None:
        estilos.aviso("Operacion cancelada.")
        return

    marcador_visitante = validaciones.validar_entero("Marcador del equipo visitante: ", minimo=0)
    if marcador_visitante is None:
        estilos.aviso("Operacion cancelada.")
        return

    arbitro = validaciones.validar_texto("Nombre del arbitro: ")
    if arbitro is None:
        estilos.aviso("Operacion cancelada.")
        return

    sede = validaciones.validar_texto("Nombre/ciudad de la sede: ")
    if sede is None:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = """
            INSERT INTO partido
            (fk_codigo_equipo_local, fk_codigo_equipo_visitante, fecha, hora,
             marcador_local, marcador_visitante, arbitro, sede)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(consulta, (codigo_local, codigo_visitante, fecha, hora,
                                   marcador_local, marcador_visitante, arbitro, sede))
        conexion.commit()
        estilos.exito("\nPartido registrado correctamente.")
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo registrar el partido: {error}")
    finally:
        cursor.close()
        conexion.close()


def listar_partidos():
    estilos.titulo("LISTADO DE PARTIDOS", estilos.COLOR_PARTIDO)
    conexion = connector.conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        consulta = """
            SELECT p.id_partido, el.nombre_equipo AS local, ev.nombre_equipo AS visitante,
                   p.marcador_local, p.marcador_visitante, p.fecha, p.hora, p.arbitro, p.sede
            FROM partido p
            INNER JOIN equipo el ON p.fk_codigo_equipo_local = el.codigo_equipo
            INNER JOIN equipo ev ON p.fk_codigo_equipo_visitante = ev.codigo_equipo
            ORDER BY p.fecha, p.hora
        """
        cursor.execute(consulta)
        partidos = cursor.fetchall()
        if not partidos:
            estilos.aviso("No hay partidos registrados.")
            return
        encabezados = ["ID", "Local", "Visitante", "Marc. Local", "Marc. Visit.", "Fecha", "Hora", "Arbitro", "Sede"]
        tabla = tabulate.tabulate(partidos, headers=encabezados, tablefmt="fancy_grid")
        estilos.imprimir_tabla(tabla, estilos.COLOR_PARTIDO)
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo listar los partidos: {error}")
    finally:
        cursor.close()
        conexion.close()


def actualizar_partido():
    estilos.titulo("ACTUALIZAR PARTIDO", estilos.COLOR_PARTIDO)
    listar_partidos()
    estilos.aviso("\nEscribe el ID del partido que quieres actualizar (o 'volver' para cancelar).\n")

    id_partido = validaciones.validar_entero("ID del partido a actualizar: ", minimo=1)
    if id_partido is None:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM partido WHERE id_partido = %s", (id_partido,))
        partido_encontrado = cursor.fetchone()
        if partido_encontrado is None:
            estilos.aviso("No existe ningun partido con ese ID.")
            return

        marcador_local = validaciones.validar_entero("Nuevo marcador del equipo local: ", minimo=0)
        if marcador_local is None:
            estilos.aviso("Operacion cancelada.")
            return

        marcador_visitante = validaciones.validar_entero("Nuevo marcador del equipo visitante: ", minimo=0)
        if marcador_visitante is None:
            estilos.aviso("Operacion cancelada.")
            return

        arbitro = validaciones.validar_texto("Nuevo nombre del arbitro: ")
        if arbitro is None:
            estilos.aviso("Operacion cancelada.")
            return

        sede = validaciones.validar_texto("Nueva sede: ")
        if sede is None:
            estilos.aviso("Operacion cancelada.")
            return

        consulta = """
            UPDATE partido
            SET marcador_local = %s, marcador_visitante = %s, arbitro = %s, sede = %s
            WHERE id_partido = %s
        """
        cursor.execute(consulta, (marcador_local, marcador_visitante, arbitro, sede, id_partido))
        conexion.commit()
        estilos.exito("\nPartido actualizado correctamente.")
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo actualizar el partido: {error}")
    finally:
        cursor.close()
        conexion.close()


def eliminar_partido():
    estilos.titulo("ELIMINAR PARTIDO", estilos.COLOR_PARTIDO)
    listar_partidos()
    estilos.aviso("\nEscribe el ID del partido que quieres eliminar (o 'volver' para cancelar).\n")

    id_partido = validaciones.validar_entero("ID del partido a eliminar: ", minimo=1)
    if id_partido is None:
        estilos.aviso("Operacion cancelada.")
        return

    confirmacion = validaciones.confirmar_accion(f"¿Seguro que deseas eliminar el partido #{id_partido}?")
    if not confirmacion:
        estilos.aviso("Operacion cancelada.")
        return

    conexion = connector.conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM partido WHERE id_partido = %s", (id_partido,))
        conexion.commit()
        if cursor.rowcount == 0:
            estilos.aviso("No existe ningun partido con ese ID.")
        else:
            estilos.exito("\nPartido eliminado correctamente.")
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo eliminar el partido: {error}")
    finally:
        cursor.close()
        conexion.close()


def tabla_posiciones():
    # <-- RETO OPCIONAL (BONUS): partidos jugados, ganados y perdidos por equipo
    estilos.titulo("TABLA DE POSICIONES (BONUS)", estilos.COLOR_POSICIONES)
    conexion = connector.conectar()
    if conexion is None:
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT codigo_equipo, nombre_equipo FROM equipo ORDER BY nombre_equipo")
        equipos = cursor.fetchall()
        if not equipos:
            estilos.aviso("No hay equipos registrados.")
            return

        tabla = []
        for codigo_equipo, nombre_equipo in equipos:
            cursor.execute("""
                SELECT marcador_local, marcador_visitante, fk_codigo_equipo_local
                FROM partido
                WHERE fk_codigo_equipo_local = %s OR fk_codigo_equipo_visitante = %s
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
        tabla_texto = tabulate.tabulate(tabla, headers=encabezados, tablefmt="fancy_grid")
        estilos.imprimir_tabla(tabla_texto, estilos.COLOR_POSICIONES)
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo calcular la tabla de posiciones: {error}")
    finally:
        cursor.close()
        conexion.close()
