import colorama

# Colores y funciones de presentacion visual del sistema.
# Cada modulo (equipo, jugador, partido) tiene su propio color
# tematico, asi todo se ve ordenado y facil de distinguir.

colorama.init(autoreset=True)

# Colores tematicos por seccion
COLOR_EQUIPO = colorama.Fore.CYAN
COLOR_JUGADOR = colorama.Fore.GREEN
COLOR_PARTIDO = colorama.Fore.MAGENTA
COLOR_POSICIONES = colorama.Fore.YELLOW
COLOR_MENU = colorama.Fore.LIGHTBLUE_EX

# Colores de mensajes generales
COLOR_EXITO = colorama.Fore.LIGHTGREEN_EX
COLOR_ERROR = colorama.Fore.LIGHTRED_EX
COLOR_AVISO = colorama.Fore.LIGHTYELLOW_EX

ANCHO_MENU = 52


def encabezado(titulo, opciones, color=COLOR_MENU):
    # opciones: lista de tuplas (texto, color_de_la_opcion)
    negrita, reset = colorama.Style.BRIGHT, colorama.Style.RESET_ALL
    print(f"{color}{negrita}╔{'═' * ANCHO_MENU}╗")
    print(f"{color}{negrita}║{titulo.center(ANCHO_MENU)}║")
    print(f"{color}{negrita}╠{'═' * ANCHO_MENU}╣")
    for texto, color_opcion in opciones:
        linea = f" {texto}".ljust(ANCHO_MENU)
        print(f"{color}{negrita}║{reset}{color_opcion}{linea}{reset}{color}{negrita}║")
    print(f"{color}{negrita}╚{'═' * ANCHO_MENU}╝{reset}")


def titulo(mensaje, color):
    print(f"\n{color}{colorama.Style.BRIGHT}--- {mensaje} ---{colorama.Style.RESET_ALL}")


def imprimir_tabla(texto_tabla, color):
    print(f"{color}{texto_tabla}{colorama.Style.RESET_ALL}")


def exito(mensaje):
    print(f"{COLOR_EXITO}{mensaje}{colorama.Style.RESET_ALL}")


def error(mensaje):
    print(f"{COLOR_ERROR}{mensaje}{colorama.Style.RESET_ALL}")


def aviso(mensaje):
    print(f"{COLOR_AVISO}{mensaje}{colorama.Style.RESET_ALL}")
