class Memoria:
    """Simula una RAM de 100 MB con asignacion continua dinamica (first-fit)."""

    TOTAL_MB = 100

    def __init__(self):
        self.bloques = []

    def asignar(self, pid, tamano):
        """Busca el primer hueco donde quepa el proceso. Si no hay, Out of Memory."""
        inicio = 0
        for b in sorted(self.bloques, key=lambda b: b["inicio"]):
            if b["inicio"] - inicio >= tamano:
                break
            inicio = b["inicio"] + b["tamano"]

        if inicio + tamano > self.TOTAL_MB:
            raise MemoryError(
                F"Out of Memory: el proceso {pid} de tamaño {tamano} MB."
                f"y solo hay {self.libre()} MB libres.")

        self.bloques.append({"pid": pid, "inicio": inicio, "tamano": tamano})
        return inicio

    def liberar(self, pid):
        """Libera la memoria que ocupaba un proceso."""
        self.bloques = [b for b in self.bloques if b["pid"] != pid]

    def usada(self):
        return sum(b["tamano"] for b in self.bloques)

    def libre(self):
        return self.TOTAL_MB - self.usada()

    def mostrar(self):
        print(f"\n--- RAM: {self.usada()}/{self.TOTAL_MB} MB usados ---")
        if not self.bloques:
            print("Memoria vacia.")
        for b in sorted(self.bloques, key=lambda b: b["inicio"]):
            fin = b["inicio"] + b["tamano"] - 1
            print(f"PID: {b['pid']}: {b['inicio']}MB - {fin}MB ({b['tamano']} MB)")