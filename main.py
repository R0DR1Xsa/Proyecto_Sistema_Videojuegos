import os
from equipo import registrar_equipo, listar_equipos, actualizar_equipo, eliminar_equipo
from jugador import registrar_jugador, listar_jugadores, actualizar_jugador, eliminar_jugador
from partido import registrar_partido, listar_partidos, actualizar_partido, eliminar_partido, tabla_posiciones

# main.py
# Menu principal del sistema de torneo de videojuegos

def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def encabezado(titulo):
    limpiar_pantalla()
    print("╔" + "═" * 50 + "╗")
    print("║" + titulo.center(50) + "║")
    print("╚" + "═" * 50 + "╝")


def menu_equipos():
    while True:
        encabezado("GESTION DE EQUIPOS")
        print("1. Registrar equipo")
        print("2. Listar equipos")
        print("3. Actualizar equipo")
        print("4. Eliminar equipo")
        print("5. Volver al menu principal")
        print("-" * 52)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            registrar_equipo()
        elif opcion == "2":
            listar_equipos()
        elif opcion == "3":
            actualizar_equipo()
        elif opcion == "4":
            eliminar_equipo()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")
        os.system("pause") if os.name == "nt" else input("\nPresiona ENTER para continuar...")


def menu_jugadores():
    while True:
        encabezado("GESTION DE JUGADORES")
        print("1. Registrar jugador")
        print("2. Listar jugadores")
        print("3. Actualizar jugador")
        print("4. Eliminar jugador")
        print("5. Volver al menu principal")
        print("-" * 52)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            registrar_jugador()
        elif opcion == "2":
            listar_jugadores()
        elif opcion == "3":
            actualizar_jugador()
        elif opcion == "4":
            eliminar_jugador()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")
        os.system("pause") if os.name == "nt" else input("\nPresiona ENTER para continuar...")


def menu_partidos():
    while True:
        encabezado("GESTION DE PARTIDOS")
        print("1. Registrar partido")
        print("2. Listar partidos")
        print("3. Actualizar partido")
        print("4. Eliminar partido")
        print("5. Volver al menu principal")
        print("-" * 52)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            registrar_partido()
        elif opcion == "2":
            listar_partidos()
        elif opcion == "3":
            actualizar_partido()
        elif opcion == "4":
            eliminar_partido()
        elif opcion == "5":
            break
        else:
            print("Opcion invalida.")
        os.system("pause") if os.name == "nt" else input("\nPresiona ENTER para continuar...")


def menu_principal():
    while True:
        encabezado("TORNEO DE VIDEOJUEGOS")
        print("1. Gestionar equipos")
        print("2. Gestionar jugadores")
        print("3. Gestionar partidos")
        print("4. Tabla de posiciones (Bonus)")
        print("5. Salir")
        print("-" * 52)
        opcion = input("Selecciona una opcion: ").strip()

        if opcion == "1":
            menu_equipos()
        elif opcion == "2":
            menu_jugadores()
        elif opcion == "3":
            menu_partidos()
        elif opcion == "4":
            tabla_posiciones()
            os.system("pause") if os.name == "nt" else input("\nPresiona ENTER para continuar...")
        elif opcion == "5":
            print("\nSaliendo del sistema... ¡Hasta la proxima!")
            break
        else:
            print("Opcion invalida.")
            os.system("pause") if os.name == "nt" else input("\nPresiona ENTER para continuar...")


if __name__ == "__main__":
    menu_principal()
