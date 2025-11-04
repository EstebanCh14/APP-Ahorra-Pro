# servicio_transaccion/TransactionServiceImpl.py
from typing import List
import datetime
import numpy as np

from common.models.transaccion import Transaccion
from common.utils import Subject
from servicio_transaccion.TransactionFactory import ITransaccionFactory
from servicio_transaccion.TransactionRepository import TransactionRepository


class LogicaFinanciera(Subject):
    """
    Servicio de transacciones (microservicio de dominio).
    Hereda de Subject para notificar cambios (Observer).
    """
    def __init__(self,
                 factory: ITransaccionFactory,
                 repository: TransactionRepository) -> None:
        super().__init__()
        self._factory = factory
        self._repository = repository
        self._cargar_datos_ejemplo()

    # --- Datos de ejemplo (igual que en el monolito) ---
    def _cargar_datos_ejemplo(self) -> None:
        fecha_base = datetime.date.today() - datetime.timedelta(days=90)
        for i in range(3):
            desplazamiento_mes = i * 30
            self.agregar_transaccion(
                fecha_base + datetime.timedelta(days=desplazamiento_mes + 1),
                "Salario Mensual",
                2500,
                "Ingreso"
            )
            self.agregar_transaccion(
                fecha_base + datetime.timedelta(days=desplazamiento_mes + 2),
                "Alquiler",
                -1200,
                "Vivienda"
            )
            self.agregar_transaccion(
                fecha_base + datetime.timedelta(days=desplazamiento_mes + 5),
                "Supermercado",
                float(-150 - np.random.rand() * 20),
                "Alimentación"
            )
            self.agregar_transaccion(
                fecha_base + datetime.timedelta(days=desplazamiento_mes + 10),
                "Transporte",
                float(-50 - np.random.rand() * 10),
                "Transporte"
            )
            self.agregar_transaccion(
                fecha_base + datetime.timedelta(days=desplazamiento_mes + 15),
                "Restaurante",
                float(-75 - np.random.rand() * 30),
                "Ocio"
            )

    # --- API del microservicio ---
    def agregar_transaccion(self,
                            fecha: datetime.date,
                            descripcion: str,
                            monto: float,
                            categoria: str) -> bool:
        transaccion = self._factory.crear(fecha, descripcion, monto, categoria)
        self._repository.agregar(transaccion)

        # Notificamos a los observadores (UI) que hubo un cambio
        self.notify("TRANSACCION_AGREGADA", transaccion)
        return True

    def obtener_transacciones(self) -> List[Transaccion]:
        return self._repository.obtener_todas()

    # Acceso al repositorio (para otros microservicios, como reporte/predicción)
    @property
    def repository(self) -> TransactionRepository:
        return self._repository
