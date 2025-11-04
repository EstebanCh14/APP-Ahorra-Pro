# servicio_prediccion/ServicioPrediccion.py
from typing import Optional, Tuple

import matplotlib.pyplot as plt

from servicio_transaccion.TransactionRepository import TransactionRepository
from servicio_prediccion.SklearnAdapter import SklearnPredictorAdapter


class ServicioPrediccion:
    """
    Microservicio que orquesta la predicción usando el Adapter de sklearn.
    """
    def __init__(self,
                repository: TransactionRepository,
                adapter: SklearnPredictorAdapter) -> None:
        self._repository = repository
        self._adapter = adapter

    def analisis_predictivo(self,
                            dias_a_predecir: int = 30
                            ) -> Tuple[Optional[plt.Figure], Optional[str]]:
        transacciones = self._repository.obtener_todas()
        return self._adapter.analizar_gastos(transacciones, dias_a_predecir)
