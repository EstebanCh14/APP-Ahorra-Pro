# servicio_prediccion/SklearnAdapter.py
from typing import Optional, Tuple, List

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend("TkAgg")
from sklearn.linear_model import LinearRegression

from common.models.transaccion import Transaccion


class SklearnPredictorAdapter:
    """
    Adapter que encapsula la lógica de pandas + sklearn
    para que el servicio de predicción no dependa directamente
    de la librería externa.

    Expone un método analizar_gastos que recibe transacciones
    y devuelve (Figura, mensaje_error).
    """

    def __init__(self) -> None:
        self._model = LinearRegression()

    def analizar_gastos(self,
                        transacciones: List[Transaccion],
                        dias_a_predecir: int = 30
                        ) -> Tuple[Optional[plt.Figure], Optional[str]]:

        if len(transacciones) < 10:
            return None, "No hay suficientes datos para realizar un análisis predictivo."

        # Convertir a DataFrame
        dataframe = pd.DataFrame([{
            "fecha": t.fecha,
            "descripcion": t.descripcion,
            "monto": t.monto,
            "categoria": t.categoria
        } for t in transacciones])
        dataframe["fecha"] = pd.to_datetime(dataframe["fecha"])

        # Filtrar solo gastos (< 0)
        gastos = dataframe[dataframe["monto"] < 0].copy()
        if gastos.empty:
            return None, "No hay gastos registrados para el análisis predictivo."

        gastos["monto"] = gastos["monto"].abs()

        # Agrupar por día
        gastos_diarios = (
            gastos
            .set_index("fecha")
            .resample("D")["monto"]
            .sum()
            .reset_index()
        )

        gastos_diarios = gastos_diarios[gastos_diarios["monto"] > 0]
        if len(gastos_diarios) < 2:
            return None, "No hay suficientes días con gastos para la predicción."

        gastos_diarios["dias_desde_inicio"] = (
            gastos_diarios["fecha"] - gastos_diarios["fecha"].min()
        ).dt.days

        X = gastos_diarios[["dias_desde_inicio"]]
        y = gastos_diarios["monto"]

        # Entrenamos el modelo
        self._model.fit(X, y)

        ultimo_dia = int(X["dias_desde_inicio"].max())
        dias_futuros = np.arange(ultimo_dia + 1,
                                ultimo_dia + 1 + dias_a_predecir).reshape(-1, 1)

        gastos_predichos = self._model.predict(dias_futuros)
        gastos_predichos[gastos_predichos < 0] = 0

        # Creamos la figura de Matplotlib
        figura, ax = plt.subplots(figsize=(10, 6))

        # Históricos
        ax.scatter(gastos_diarios["fecha"], y,
                label="Gastos Históricos", alpha=0.6)

        # Tendencia ajustada a las fechas históricas
        ax.plot(
            gastos_diarios["fecha"],
            self._model.predict(X),
            linewidth=2,
            label="Tendencia"
        )

        # Predicciones
        fechas_futuras = (
            pd.to_datetime(gastos_diarios["fecha"].min())
            + pd.to_timedelta(dias_futuros.flatten(), unit="D")
        )

        ax.plot(
            fechas_futuras,
            gastos_predichos,
            linestyle="--",
            linewidth=2,
            label=f"Predicción {dias_a_predecir} días"
        )

        ax.set_title(
            f"Análisis Predictivo de Gastos\nPredicción Total: ${gastos_predichos.sum():,.2f}",
            fontsize=14
        )
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Monto de Gasto ($)")
        ax.legend()
        figura.autofmt_xdate()
        plt.tight_layout()

        return figura, None
