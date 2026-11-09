ACC = None
PC = 0
ram = []

CAPACIDAD = 0
BITS = 0
MAXIMO = 0


def configurar_memoria():
    global CAPACIDAD, BITS, MAXIMO, ram

    print("\n===== CONFIGURACION DE MEMORIA =====")

    while True:
        try:
            CAPACIDAD = int(input("Cantidad de posiciones RAM: "))
            if CAPACIDAD > 0:
                break
            print("Debe ser mayor que cero.")
        except ValueError:
            print("Ingrese un numero valido.")

    while True:
        try:
            BITS = int(input("Bits por posicion: "))
            if BITS > 0:
                break
            print("Debe ser mayor que cero.")
        except ValueError:
            print("Ingrese un numero valido.")

    MAXIMO = (2 ** BITS) - 1
    ram = [None] * CAPACIDAD

    capacidad_bits = CAPACIDAD * BITS
    capacidad_bytes = capacidad_bits / 8

    print("\nCONFIGURACION CREADA")
    print(f"Posiciones RAM: {CAPACIDAD}")
    print(f"Bits por palabra: {BITS}")
    print(f"Valor maximo: {MAXIMO}")
    print(f"Capacidad total: {capacidad_bits} bits")
    print(f"Capacidad total: {capacidad_bytes} bytes")


def pedir_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("Ingrese un numero valido.")


def mostrar_memoria():

    print("\n========== MEMORIA RAM ==========")

    bits_direccion = max(1, (CAPACIDAD - 1).bit_length())

    encabezado = (
        "DIR(dec) | DIR(bin) | DATO(dec) | DATO(bin)"
    )

    print(encabezado)
    print("-" * len(encabezado))

    for direccion, dato in enumerate(ram):

        dir_bin = format(direccion, f"0{bits_direccion}b")

        if dato is None:
            dato_dec = "Vacia"
            dato_bin = "-" * BITS
        else:
            dato_dec = str(dato)
            dato_bin = format(dato, f"0{BITS}b")

        print(
            f"{direccion:8} | "
            f"{dir_bin:8} | "
            f"{dato_dec:9} | "
            f"{dato_bin}"
        )

    ocupadas = sum(x is not None for x in ram)

    print(f"\nPosiciones ocupadas: {ocupadas}/{CAPACIDAD}")


def escribir():

    direccion = pedir_entero(
        f"Direccion (0-{CAPACIDAD - 1}): "
    )

    if direccion < 0 or direccion >= CAPACIDAD:
        print("Direccion fuera de rango.")
        return

    dato = pedir_entero(
        f"Dato (0-{MAXIMO}): "
    )

    if dato < 0 or dato > MAXIMO:
        print("Dato fuera de rango.")
        return

    anterior = ram[direccion]

    ram[direccion] = dato

    if anterior is None:
        print("Dato guardado correctamente.")
    else:
        print(
            f"Direccion {direccion} actualizada "
            f"de {anterior} a {dato}"
        )


def leer():

    direccion = pedir_entero(
        f"Direccion (0-{CAPACIDAD - 1}): "
    )

    if direccion < 0 or direccion >= CAPACIDAD:
        print("Direccion fuera de rango.")
        return

    dato = ram[direccion]

    if dato is None:
        print("Posicion vacia.")
        return

    print(f"Decimal : {dato}")
    print(f"Binario : {format(dato, f'0{BITS}b')}")


def ejecutar_programa():

    global ACC
    global PC

    historial = []

    PC = 0

    print("\n=== MODO FETCH-DECODE-EXECUTE ===")
    print("Escriba SALIR para terminar")
    print("Operaciones:")
    print("LOAD d | ADD d | SUB d | MUL d | STORE d | INC")

    while True:

        print("\n--------------------------------")
        print(f"PC = {PC}")
        print(f"ACC = {ACC}")
        print("--------------------------------")

        linea = input("Instruccion: ").upper().strip()

        if linea == "SALIR":
            break

        partes = linea.split()

        operacion = None
        direccion = None

        if len(partes) == 1:

            if partes[0] != "INC":
                print("Instruccion invalida.")
                continue

            operacion = "INC"

        elif len(partes) == 2:

            operacion = partes[0]

            try:
                direccion = int(partes[1])
            except ValueError:
                print("Direccion invalida.")
                continue

            if direccion < 0 or direccion >= CAPACIDAD:
                print("Direccion fuera de rango.")
                continue

        else:
            print("Formato incorrecto.")
            continue

        print("\nFETCH")
        print(f"PC = {PC}")
        print(f"Instruccion obtenida: {linea}")

        print("\nDECODE")
        print(f"Operacion: {operacion}")

        if direccion is not None:
            print(f"Operando: {direccion}")

        print("\nEXECUTE")

        acc_antes = ACC
        resultado = ""

        try:

            if operacion == "LOAD":

                if ram[direccion] is None:
                    print("La direccion esta vacia.")
                    continue

                ACC = ram[direccion]

                resultado = f"ACC = {ACC}"

            elif operacion == "ADD":

                if ACC is None:
                    print("ACC vacio.")
                    continue

                if ram[direccion] is None:
                    print("La direccion esta vacia.")
                    continue

                valor = ram[direccion]

                ACC = (ACC + valor) % (MAXIMO + 1)

                resultado = f"{acc_antes} + {valor} = {ACC}"

            elif operacion == "SUB":

                if ACC is None:
                    print("ACC vacio.")
                    continue

                if ram[direccion] is None:
                    print("La direccion esta vacia.")
                    continue

                valor = ram[direccion]

                ACC = (ACC - valor) % (MAXIMO + 1)

                resultado = f"{acc_antes} - {valor} = {ACC}"

            elif operacion == "MUL":

                if ACC is None:
                    print("ACC vacio.")
                    continue

                if ram[direccion] is None:
                    print("La direccion esta vacia.")
                    continue

                valor = ram[direccion]

                ACC = (ACC * valor) % (MAXIMO + 1)

                resultado = f"{acc_antes} * {valor} = {ACC}"

            elif operacion == "INC":

                if ACC is None:
                    print("ACC vacio.")
                    continue

                ACC = (ACC + 1) % (MAXIMO + 1)

                resultado = f"{acc_antes} + 1 = {ACC}"

            elif operacion == "STORE":

                if ACC is None:
                    print("ACC vacio.")
                    continue

                ram[direccion] = ACC

                resultado = f"RAM[{direccion}] = {ACC}"

            print(resultado)

            historial.append(
                [
                    PC,
                    linea,
                    acc_antes,
                    ACC,
                    resultado
                ]
            )

            PC += 1

        except Exception as e:
            print("Error:", e)

    print("\n===== HISTORIAL =====")

    for fila in historial:

        print(
            f"PC={fila[0]} | "
            f"{fila[1]} | "
            f"ACC Antes={fila[2]} | "
            f"ACC Despues={fila[3]}"
        )
def reiniciar():

    global ACC
    global PC
    global ram

    respuesta = input(
        "Borrar memoria y CPU? (s/n): "
    ).lower()

    if respuesta == "s":

        ram = [None] * CAPACIDAD
        ACC = None
        PC = 0

        print("Sistema reiniciado.")


def menu():

    while True:

        print("\n========== SIMULADOR ==========")
        print("1. Mostrar memoria")
        print("2. Escribir dato")
        print("3. Leer dato")
        print("4. Ejecutar programa")
        print("5. Reiniciar")
        print("0. Salir")

        opcion = input("Opcion: ")

        if opcion == "1":
            mostrar_memoria()

        elif opcion == "2":
            escribir()

        elif opcion == "3":
            leer()

        elif opcion == "4":
            ejecutar_programa()

        elif opcion == "5":
            reiniciar()

        elif opcion == "0":
            print("Hasta luego.")
            break

        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    configurar_memoria()
    menu()