# servicio_transaccion/TransactionRepository.py
from typing import List
from common.models.transaccion import Transaccion


class TransactionRepository:
    """
    Repositorio en memoria para almacenar transacciones.
    Si más adelante quieres persistencia en BD, se cambia aquí.
    """
    def __init__(self) -> None:
        self._transacciones: List[Transaccion] = []

    def agregar(self, transaccion: Transaccion) -> None:
        self._transacciones.append(transaccion)
        # Ordenar por fecha descendente (más reciente primero)
        self._transacciones.sort(key=lambda t: t.fecha, reverse=True)

    def obtener_todas(self) -> List[Transaccion]:
        # Se devuelve una copia para evitar modificar la lista interna.
        return list(self._transacciones)
