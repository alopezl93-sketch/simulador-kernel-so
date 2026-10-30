from collections import deque


class Semaforo:
    """Semaforo binario con wait() y signal() y cola de espera."""
    def __init__(self):
        self.valor = 1
        self.dueno = None
        self.cola_espera = deque()

    def wait(self, pcb):
        """Intentar entrar a la sección crítica."""
        if self.valor == 1:
            self.valor = 0
            self.dueno = pcb.pid
            print(f"PID {pcb.pid} ENTRA a la seccion critica.")
            return True
        pcb.estado = "Bloqueado"
        self.cola_espera.append(pcb)
        print(f"Seccion critica OCUPADA por PID {self.dueno}."
              f"PID {pcb.pid} enviado a la cola de espera.")
        return False

    def signal(self, pcb):
        """Sale de la seccion critica y despierta al siguiente en espera."""
        if self.cola_espera:
            siguiente = self.cola_espera.popleft()
            siguiente.estado = "Listo"
            self.dueno = siguiente.pid
            print(f"PID {siguiente.pid} despierta y Entra a la seccion critica.")
        else:
            self.valor = 1
            self.dueno = None      