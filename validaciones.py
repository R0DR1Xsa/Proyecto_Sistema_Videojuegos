import re

# Funciones reutilizables para validar los datos que ingresa
# el usuario por teclado.
#
# en cualquier campo de texto/numero/fecha/hora, el usuario
# puede escribir "volver" para cancelar la operacion en curso y
# regresar al menu anterior. Cuando eso pasa, la funcion retorna
# None, y quien la llama debe revisar ese None y hacer return.

PALABRA_CANCELAR = "volver"


def es_volver(dato):
    return dato.strip().lower() == PALABRA_CANCELAR


def validar_texto(mensaje):
    while True:
        dato = input(mensaje).strip()
        if es_volver(dato):
            return None
        if dato == "":
            print("Este campo no puede estar vacio. Intenta de nuevo (o escribe 'volver').")
            continue
        return dato


def validar_entero(mensaje, minimo=None):
    while True:
        dato = input(mensaje).strip()
        if es_volver(dato):
            return None
        if not dato.isdigit():
            print("Debes ingresar un numero entero valido (o escribe 'volver').")
            continue
        valor = int(dato)
        if minimo is not None and valor < minimo:
            print(f"El valor debe ser mayor o igual a {minimo}.")
            continue
        return valor


def validar_fecha(mensaje):
    # Formato esperado: AAAA-MM-DD
    while True:
        dato = input(mensaje).strip()
        if es_volver(dato):
            return None
        partes = dato.split("-")
        if len(partes) == 3 and all(p.isdigit() for p in partes):
            anio, mes, dia = partes
            if len(anio) == 4 and 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31:
                return dato
        print("Formato de fecha invalido. Usa el formato AAAA-MM-DD (ej: 2026-09-10), o escribe 'volver'.")


def validar_hora(mensaje):
    # Formato esperado: HH:MM
    while True:
        dato = input(mensaje).strip()
        if es_volver(dato):
            return None
        partes = dato.split(":")
        if len(partes) == 2 and all(p.isdigit() for p in partes):
            hora, minuto = partes
            if 0 <= int(hora) <= 23 and 0 <= int(minuto) <= 59:
                return dato + ":00"
        print("Formato de hora invalido. Usa el formato HH:MM (ej: 17:30), o escribe 'volver'.")


def confirmar_accion(mensaje):
    while True:
        respuesta = input(f"{mensaje} (s/n, o 'volver' para cancelar): ").strip().lower()
        if es_volver(respuesta):
            return None
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta invalida. Escribe 's' para si, 'n' para no, o 'volver' para cancelar.")


# Patron de codigo de equipo: 2 a 4 letras seguidas de 2 a 4 numeros.
# Ejemplos validos: EQ01, EQU01, LOB99
PATRON_CODIGO_EQUIPO = re.compile(r'^[A-Z]{2,4}[0-9]{2,4}$')


def validar_codigo_equipo(mensaje):
    # Se usa SOLO al registrar un equipo nuevo, para forzar que todos
    # los codigos tengan la misma escritura (ej: EQ01, EQ02...).
    while True:
        dato = input(mensaje).strip().upper()
        if es_volver(dato):
            return None
        if dato == "":
            print("Este campo no puede estar vacio (o escribe 'volver').")
            continue
        if not PATRON_CODIGO_EQUIPO.match(dato):
            print("Formato invalido. Usa letras seguidas de numeros, ej: EQ01 (o escribe 'volver').")
            continue
        return dato
