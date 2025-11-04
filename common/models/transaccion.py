import datetime
from dataclasses import dataclass

@dataclass
class Transaccion:
    """
    Entidad base de transacción.
    """
    fecha: datetime.date
    descripcion: str
    monto: float
    categoria: str

    def es_ingreso(self) -> bool:
        return self.monto >= 0


class Ingreso(Transaccion):
    """
    Transacción de tipo ingreso.
    """
    pass


class Gasto(Transaccion):
    """
    Transacción de tipo gasto.
    """
    pass
