# gateway/AppGraficaFinanzas/main.py
from servicio_transaccion.TransactionFactory import TransaccionFactory
from servicio_transaccion.TransactionRepository import TransactionRepository
from servicio_transaccion.TransactionServiceImpl import LogicaFinanciera

from servicio_reporte.GeneradorReporte import GeneradorReporte
from servicio_reporte.ControladorResumen import ControladorResumen

from servicio_prediccion.SklearnAdapter import SklearnPredictorAdapter
from servicio_prediccion.ServicioPrediccion import ServicioPrediccion


class FinanzasGateway:
    """
    Gateway / fachada que expone una interfaz sencilla para la UI.
    Aquí se "conectan" los microservicios.
    """
    def __init__(self) -> None:
        # Infra básica
        self._repository = TransactionRepository()
        self._factory = TransaccionFactory()

        # Microservicio de transacciones (Subject del Observer)
        self._logica_financiera = LogicaFinanciera(self._factory, self._repository)

        # Microservicio de reporte
        self._generador_reporte = GeneradorReporte()
        self._controlador_resumen = ControladorResumen(self._repository,
                                                    self._generador_reporte)

        # Microservicio de predicción
        self._sklearn_adapter = SklearnPredictorAdapter()
        self._servicio_prediccion = ServicioPrediccion(self._repository,
                                                    self._sklearn_adapter)

    # --- Exposición de servicios a la UI ---

    @property
    def logica_financiera(self) -> LogicaFinanciera:
        return self._logica_financiera

    def agregar_transaccion(self, *args, **kwargs) -> bool:
        return self._logica_financiera.agregar_transaccion(*args, **kwargs)

    def obtener_transacciones(self):
        return self._logica_financiera.obtener_transacciones()

    def obtener_resumen_por_categoria(self) -> str:
        return self._controlador_resumen.obtener_resumen_por_categoria()

    def analisis_predictivo(self, dias_a_predecir: int = 30):
        return self._servicio_prediccion.analisis_predictivo(dias_a_predecir)


def crear_gateway() -> FinanzasGateway:
    """
    Helper para crear el gateway desde la UI.
    """
    return FinanzasGateway()
