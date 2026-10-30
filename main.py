from pcb import PCB
from memoria import Memoria
from planificador import Planificador
from semaforo import Semaforo
from deadlock import GestorRecursos

memoria = Memoria()
planificador = Planificador(memoria)
semaforo = Semaforo()
recursos = GestorRecursos()
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

def buscar_pcb(mensaje):
    pid = leer_entero(mensaje)
    pcb = next ((p for p in procesos if p.pid == pid), None)
    if pcb is None:
        print("Error: ese PID no existe.")
    return pcb

def simulador_deadlock():
    """Fuerza el bloque: A retiene R1 y pide R2; B retiene R2 y pide R1."""
    print("\n--- Simulacion de Deadlock ---")
    a = buscar_pcb("PID del Proceso A: ")
    if a is None:
        return
    b = buscar_pcb("PID del proceso B:")
    if b is None:
        return
    if a.pid == b.pid:
        print("Error: deben ser dos procesos distintos.")
        return
    recursos.solicitar(a, 1)
    recursos.solicitar(b, 2)
    recursos.solicitar(a, 2)
    recursos.solicitar(b, 1)
    verificar_deadlock()

def verificar_deadlock():
    ciclo = recursos.detectar_deadlock()
    if ciclo:
        print(f"\n[ALERTA] DEADLOCK detectado entre los procesos: {ciclo}")
        print("Usa la opcion 9 para abortar uno de ellos.")
    else:
        print("\nNo hay deadlock.")

def abortar_proceso():
    print("\n--- Abortar proceso ---")
    pcb = buscar_pcb("PID del proceso a abortar: ")
    if pcb is None:
        return
    recursos.liberar_todos(pcb.pid)
    memoria.liberar(pcb.pid)
    pcb.estado = "terminado (abortado)"
    print (f"PID {pcb.pid} abortado forzosamente.")
    verificar_deadlock()


def menu():
        while True:
            print("\n--- SIMULADOR DE KERNEL ---")
            print("1. Ingresar proceso")
            print("2. Ver procesos (PCB)")
            print("3. Ver memoria RAM")
            print("4. Ejecutar Round Robin")
            print("5. Entrar a sección crítica (wait)")
            print("6. Salir de seccion critica (signal)")
            print("7. simular Deadlock")
            print("8. Detectar Deadlock")
            print("9. Abortar un proceso")
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
            elif opcion == "7":
                simulador_deadlock()
            elif opcion == "8":
                verificar_deadlock()
            elif opcion == "9":
                abortar_proceso()
            elif opcion == "0":
                print("Saliendo...")
                break
            else:
                print("Opción inválida.")


if __name__ == "__main__":
    menu()
