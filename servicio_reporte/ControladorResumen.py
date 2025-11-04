# servicio_reporte/ControladorResumen.py
from servicio_transaccion.TransactionRepository import TransactionRepository
from servicio_reporte.GeneradorReporte import GeneradorReporte


class ControladorResumen:
    """
    Servicio de alto nivel para obtener el resumen.
    Usa el repositorio de transacciones y el GeneradorReporte.
    """
    def __init__(self,
                repository: TransactionRepository,
                generador: GeneradorReporte) -> None:
        self._repository = repository
        self._generador = generador

    def obtener_resumen_por_categoria(self) -> str:
        transacciones = self._repository.obtener_todas()
        return self._generador.generar_resumen(transacciones)
