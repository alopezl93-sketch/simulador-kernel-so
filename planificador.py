from collections import deque


class Planificador:
    """Planificador Round Robin con quantum fijo."""

    QUANTUM = 3

    def __init__(self, memoria):
        self.memoria = memoria
        self.cola_listos = deque()
        self.tiempo = 0
        self.cambios_context = 0

    def agregar(self, pcb):
        """Mete un proceso a la cola de listos."""
        pcb.estado = "listo"
        self.cola_listos.append(pcb)

    def ejecutar(self):
        """Ejecuta Round Robin hasta que la cola quede vacia."""
        if not self.cola_listos:
            print("No hay procesos listos para ejecutar.")
            return

        print(f"\n=== ROUND ROBIN (quantum = {self.QUANTUM}) ===")
        while self.cola_listos:
            pcb = self.cola_listos.popleft()
            pcb.estado = "Ejecutando"


            uso = min(self.QUANTUM, pcb.rafaga_restante)
            inicio = self.tiempo
            self.tiempo += uso
            pcb.rafaga_restante -= uso


            print(f"[t={inicio}-{self.tiempo}] PID {pcb.pid} ejecuta {uso} u."
            f"Restante: {pcb.rafaga_restante} u.")

            if pcb.rafaga_restante == 0:
                pcb.estado = "Terminado"
                self.memoria.liberar(pcb.pid)
                print(f" -> PID {pcb.pid} TERMINADO. Memoria liberada.")
            else:
                pcb.estado = "listo"
                self.cola_listos.append(pcb)
                self.cambios_context += 1
                print(f" -> Cambio de contexto: PID {pcb.pid} vuelve al final de la cola.")

        print(f"\nTiempo total: {self.tiempo} | Cambios de contexto: {self.cambios_context}")