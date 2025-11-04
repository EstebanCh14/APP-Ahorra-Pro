# servicio_reporte/GeneradorReporte.py
from typing import List, Dict
from collections import defaultdict

from common.models.transaccion import Transaccion


class GeneradorReporte:
    """
    Microservicio que genera el texto de resumen
    a partir de una lista de transacciones.
    """
    def generar_resumen(self, transacciones: List[Transaccion]) -> str:
        if not transacciones:
            return "No hay transacciones para resumir."

        resumen: Dict[str, float] = defaultdict(float)
        ingreso_total: float = 0.0
        gasto_total: float = 0.0

        for transaccion in transacciones:
            if transaccion.es_ingreso():
                ingreso_total += transaccion.monto
            else:
                resumen[transaccion.categoria] += transaccion.monto
                gasto_total += transaccion.monto

        saldo = ingreso_total + gasto_total
        texto_resumen = " Resumen de Gastos por Categoría \n"

        if not resumen:
            texto_resumen += "No hay gastos registrados.\n"
        else:
            for categoria, total in sorted(resumen.items(), key=lambda item: item[1]):
                texto_resumen += f"{categoria:<20}: ${total:,.2f}\n"

        texto_resumen += (
            "\n--- Resumen General ---\n"
            f"Ingresos Totales: ${ingreso_total:,.2f}\n"
            f"Gastos Totales:   ${gasto_total:,.2f}\n"
            f"Saldo General:    ${saldo:,.2f}\n"
        )
        return texto_resumen
