class GestorRecursos:
    """Maneja dos recursos exclusivos y (R1 y R2) y detecta deadlocks."""
    def __init__(self):
        self.duenos = {1: None, 2: None}
        self.esperando = {}

    def solicitar(self, pcb, recurso):
        """Un proceso pide un recurso. Si esta ocupado, queda esperando."""
        if recurso not in self.duenos:
            print("Error: solo existen el Recurso 1 y el Recurso 2.")
            return False

        if self.duenos[recurso] is None:
            self.duenos[recurso] = pcb.pid
            self.esperando.pop(pcb.pid, None)
            print(f"PID{pcb.pid} obtiene el Recurso {recurso}.")
            return True

        if self.duenos[recurso] == pcb.pid:
            print(f"PID{pcb.pid} ya tiene el Recurso {recurso}.")
            return True

        pcb.estado = "Bloqueado"
        self.esperando[pcb.pid] = recurso
        print(f"Recurso {recurso} ocupado por PID {self.duenos[recurso]}."
              f"PID {pcb.pid} queda BLOQUEADO esperando.")
        return False

    def liberar_todos(self, pid):
        """libera todos los recursos de un proceso y los saca de la espera."""
        for r in self.duenos:
            if self.duenos[r] == pid:
                self.duenos[r] = None
                print(f"Recurso {r} liberado por PID {pid}.")
        self.esperando.pop(pid, None)

    def detectar_deadlock(self):
        """Busca un ciclo de espera circular. Devuelve lista de PIDs o None."""
        for inicio in self.esperando:
            visitados = []
            actual = inicio 
            while actual in self.esperando and actual not in visitados:
                visitados.append(actual)
                recurso = self.esperando[actual]
                actual = self.duenos[recurso]
                if actual is None:
                    break
            if actual == inicio:
                return visitados
        return None

    def mostrar(self):
        print("\n--- Estado de recursos ---")
        for r, d in self.duenos.items():
            print(f"Recurso {r}: {'libre' if d is None else 'PID ' + str(d)}")
        for pid, r in self.esperando.items():
            print(f"PID {pid} esta esperando el Recurso {r}")