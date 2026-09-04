# Funciones reutilizables para validar los datos que ingresa
# el usuario por teclado.

def validar_texto(mensaje):
    while True:
        dato = input(mensaje).strip()
        if dato == "":
            print("Este campo no puede estar vacio. Intenta de nuevo.")
            continue
        return dato


def validar_entero(mensaje, minimo=None):
    while True:
        dato = input(mensaje).strip()
        if not dato.isdigit():
            print("Debes ingresar un numero entero valido.")
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
        partes = dato.split("-")
        if len(partes) == 3 and all(p.isdigit() for p in partes):
            anio, mes, dia = partes
            if len(anio) == 4 and 1 <= int(mes) <= 12 and 1 <= int(dia) <= 31:
                return dato
        print("Formato de fecha invalido. Usa el formato AAAA-MM-DD (ej: 2026-09-10).")


def validar_hora(mensaje):
    # Formato esperado: HH:MM
    while True:
        dato = input(mensaje).strip()
        partes = dato.split(":")
        if len(partes) == 2 and all(p.isdigit() for p in partes):
            hora, minuto = partes
            if 0 <= int(hora) <= 23 and 0 <= int(minuto) <= 59:
                return dato + ":00"
        print("Formato de hora invalido. Usa el formato HH:MM (ej: 17:30).")


def confirmar_accion(mensaje):
    while True:
        respuesta = input(f"{mensaje} (s/n): ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta invalida. Escribe 's' para si o 'n' para no.")
