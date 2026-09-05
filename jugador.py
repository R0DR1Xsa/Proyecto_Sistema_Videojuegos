import tabulate

import connector, equipo, estilos, validaciones

# Operaciones CRUD para la tabla jugadores


def registrar_jugador():
    estilos.titulo("REGISTRAR NUEVO JUGADOR", estilos.COLOR_JUGADOR)
    equipo.listar_equipos()
    estilos.aviso("\nEscribe 'volver' en cualquier campo para cancelar y regresar al menu.\n")

    nickname = validaciones.validar_texto("Nickname del jugador (unico): ")
    if nickname is None:
        estilos.aviso("Operacion cancelada.")
        return

    nombre_real = validaciones.validar_texto("Nombre real: ")
    if nombre_real is None:
        estilos.aviso("Operacion cancelada.")
        return

    rol = validaciones.validar_texto("Rol dentro del juego (ej: soporte, francotirador, capitan): ")
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
    try:
        cursor = conexion.cursor()
        consulta = "INSERT INTO jugadores (nickname, nombre_real, rol, fk_codigo_equipo) VALUES (%s, %s, %s, %s)"
        cursor.execute(consulta, (nickname, nombre_real, rol, codigo_equipo))
        conexion.commit()
        estilos.exito(f"\nJugador '{nickname}' registrado correctamente.")
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo registrar el jugador: {error}")
    finally:
        cursor.close()
        conexion.close()


def listar_jugadores():
    estilos.titulo("LISTADO DE JUGADORES", estilos.COLOR_JUGADOR)
    conexion = connector.conectar()
    if conexion is None:
        return
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
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo listar los jugadores: {error}")
    finally:
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
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM jugadores WHERE nickname = %s", (nickname,))
        jugador_encontrado = cursor.fetchone()
        if jugador_encontrado is None:
            estilos.aviso("No existe ningun jugador con ese nickname.")
            return

        nuevo_nombre = validaciones.validar_texto("Nuevo nombre real: ")
        if nuevo_nombre is None:
            estilos.aviso("Operacion cancelada.")
            return

        nuevo_rol = validaciones.validar_texto("Nuevo rol: ")
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
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo actualizar el jugador: {error}")
    finally:
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
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM jugadores WHERE nickname = %s", (nickname,))
        conexion.commit()
        if cursor.rowcount == 0:
            estilos.aviso("No existe ningun jugador con ese nickname.")
        else:
            estilos.exito("\nJugador eliminado correctamente.")
    except Exception as error:
        estilos.error(f"\n[ERROR] No se pudo eliminar el jugador: {error}")
    finally:
        cursor.close()
        conexion.close()
