class PCB:
    """Bloque de control de procesos: guarda la información de cada proceso."""

    def __init__(self, pid, memoria_mb, rafaga_total):
        self.pid = pid  
        self.estado = "nuevo"  
        self.memoria_mb = memoria_mb  
        self.rafaga_total = rafaga_total 
        self.rafaga_restante = rafaga_total  

    def __str__(self):
        return (f"PID: {self.pid} | Estado: {self.estado} | Memoria: {self.memoria_mb} MB | Rafaga Total: {self.rafaga_total} | Rafaga Restante: {self.rafaga_restante}")