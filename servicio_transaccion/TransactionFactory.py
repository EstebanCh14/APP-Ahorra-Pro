# servicio_transaccion/TransactionFactory.py
from typing import Protocol
import datetime
from common.models.transaccion import Transaccion, Ingreso, Gasto


class ITransaccionFactory(Protocol):
    """
    Interfaz de la fábrica de transacciones (Factory Method).
    """
    def crear(self,
            fecha: datetime.date,
            descripcion: str,
            monto: float,
            categoria: str) -> Transaccion:
        ...


class TransaccionFactory(ITransaccionFactory):
    """
    Implementación concreta del Factory Method.
    Crea Ingreso o Gasto según el monto.
    """
    def crear(self,
            fecha: datetime.date,
            descripcion: str,
            monto: float,
            categoria: str) -> Transaccion:
        if monto >= 0:
            return Ingreso(fecha, descripcion, monto, categoria)
        return Gasto(fecha, descripcion, monto, categoria)
