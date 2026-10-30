from pcb import PCB
from memoria import Memoria
from planificador import Planificador
from semaforo import Semaforo

memoria = Memoria()
planificador = Planificador(memoria)
semaforo = Semaforo()
variable_compartida = 0
procesos = []
siguiente_pid = 1


def leer_entero(mensaje, minimo=1):
    """Pide un numero entero y valida que sea correcto (no letras, no negativos)."""
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"Error: debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print(f"Error: ingresa un numero entero valido.")


def ingresar_proceso():
    global siguiente_pid
    print("\n--- Ingresar Proceso ---")
    tamano = leer_entero("Tamaño de memoria (MB): ")
    rafaga = leer_entero("Ráfaga de CPU total: ")

    try:
        inicio = memoria.asignar(siguiente_pid, tamano)
    except MemoryError as e:
        print(f"\n[Error] {e}")
        print("Proceso rechazado")
        return

    pcb = PCB(siguiente_pid, tamano, rafaga)
    pcb.estado = "listo"
    procesos.append(pcb)
    planificador.agregar(pcb)
    print(f"\nProceso {siguiente_pid} creado en RAM (inicio: {inicio}MB).")
    siguiente_pid += 1

def ver_procesos():
        print("\n--- Procesos (PCB) ---")
        if not procesos:
            print("No hay procesos.")
        for p in procesos:
            print(p)

def seccion_critica():
    global variable_compartida
    print("\n--- Seccion critica (variable compartida) ---")
    pid = leer_entero("PID del proceso:")
    pcb = next((p for p in procesos if p.pid == pid), None)
    if pcb is None:
        print("Error: ese PID no existe.")
        return

    if semaforo.wait(pcb):
        variable_compartida += 1
        print(f"Variable compartida = {variable_compartida}")
        print ("(el proceso sigue dentro; usa la opcion 6 para liberar)")

def salir_seccion_critica():
    pid = leer_entero("PID del proceso que sale:")
    pcb = next((p for p in procesos if p.pid == pid), None)
    if pcb is None:
        print("Error: ese PID no existe.")
        return
    semaforo.signal(pcb)

def menu():
        while True:
            print("\n--- SIMULADOR DE KERNEL ---")
            print("1. Ingresar proceso")
            print("2. Ver procesos (PCB)")
            print("3. Ver memoria RAM")
            print("4. Ejecutar Round Robin")
            print("5. Entrar a sección crítica (wait)")
            print("6. Salir de seccion critica (signal)")
            print("0. Salir")
            opcion = input("Selecciona una opción: ")

            if opcion == "1":
                ingresar_proceso()
            elif opcion == "2":
                ver_procesos()
            elif opcion == "3":
                memoria.mostrar()
            elif opcion == "4":
                planificador.ejecutar()
            elif opcion == "5":
                seccion_critica()
            elif opcion == "6":
                salir_seccion_critica()
            elif opcion == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    menu()
