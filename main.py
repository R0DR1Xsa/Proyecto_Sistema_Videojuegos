import os

import colorama
import equipo, estilos, jugador, partido

# Menu principal del sistema de torneo de videojuegos


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    os.system("pause") if os.name == "nt" else input("\nPresiona ENTER para continuar...")


def menu_equipos():
    while True:
        limpiar_pantalla()
        estilos.encabezado("GESTION DE EQUIPOS", [
            ("1. Registrar equipo", estilos.COLOR_EQUIPO),
            ("2. Listar equipos", estilos.COLOR_EQUIPO),
            ("3. Actualizar equipo", estilos.COLOR_EQUIPO),
            ("4. Eliminar equipo", estilos.COLOR_EQUIPO),
            ("5. Volver al menu principal", estilos.COLOR_MENU),
        ], estilos.COLOR_EQUIPO)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            equipo.registrar_equipo()
        elif opcion == "2":
            equipo.listar_equipos()
        elif opcion == "3":
            equipo.actualizar_equipo()
        elif opcion == "4":
            equipo.eliminar_equipo()
        elif opcion == "5":
            break
        else:
            estilos.aviso("Opcion invalida.")
        pausar()


def menu_jugadores():
    while True:
        limpiar_pantalla()
        estilos.encabezado("GESTION DE JUGADORES", [
            ("1. Registrar jugador", estilos.COLOR_JUGADOR),
            ("2. Listar jugadores", estilos.COLOR_JUGADOR),
            ("3. Actualizar jugador", estilos.COLOR_JUGADOR),
            ("4. Eliminar jugador", estilos.COLOR_JUGADOR),
            ("5. Volver al menu principal", estilos.COLOR_MENU),
        ], estilos.COLOR_JUGADOR)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            jugador.registrar_jugador()
        elif opcion == "2":
            jugador.listar_jugadores()
        elif opcion == "3":
            jugador.actualizar_jugador()
        elif opcion == "4":
            jugador.eliminar_jugador()
        elif opcion == "5":
            break
        else:
            estilos.aviso("Opcion invalida.")
        pausar()


def menu_partidos():
    while True:
        limpiar_pantalla()
        estilos.encabezado("GESTION DE PARTIDOS", [
            ("1. Registrar partido", estilos.COLOR_PARTIDO),
            ("2. Listar partidos", estilos.COLOR_PARTIDO),
            ("3. Actualizar partido", estilos.COLOR_PARTIDO),
            ("4. Eliminar partido", estilos.COLOR_PARTIDO),
            ("5. Volver al menu principal", estilos.COLOR_MENU),
        ], estilos.COLOR_PARTIDO)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            partido.registrar_partido()
        elif opcion == "2":
            partido.listar_partidos()
        elif opcion == "3":
            partido.actualizar_partido()
        elif opcion == "4":
            partido.eliminar_partido()
        elif opcion == "5":
            break
        else:
            estilos.aviso("Opcion invalida.")
        pausar()


def menu_principal():
    while True:
        limpiar_pantalla()
        estilos.encabezado("TORNEO DE VIDEOJUEGOS", [
            ("1. Gestionar equipos", estilos.COLOR_EQUIPO),
            ("2. Gestionar jugadores", estilos.COLOR_JUGADOR),
            ("3. Gestionar partidos", estilos.COLOR_PARTIDO),
            ("4. Tabla de posiciones (Bonus)", estilos.COLOR_POSICIONES),
            ("5. Salir", estilos.COLOR_ERROR),
        ], estilos.COLOR_MENU)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_jugadores()
        elif opcion == "3":
            menu_partidos()
        elif opcion == "4":
            partido.tabla_posiciones()
            pausar()
        elif opcion == "5":
            estilos.exito("\nGracias por usar Nuestro Sistema ¡Hasta la proxima!")
            break
        else:
            estilos.aviso("Opcion invalida.")
            pausar()


if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        estilos.aviso("\n\nSaliste con Ctrl+C. ¡Hasta la proxima!")
    except EOFError:
        estilos.aviso("\n\nEntrada finalizada. ¡Hasta la proxima!")
