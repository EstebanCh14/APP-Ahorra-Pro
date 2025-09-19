import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from typing import List, Dict, Tuple, Optional

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from sklearn.linear_model import LinearRegression


# Modelo de Datos 
class Transaccion:

    #Representa una transacción financiera.

    def __init__(self, fecha: datetime.date, descripcion: str, monto: float, categoria: str):
        self.fecha: datetime.date = fecha
        self.descripcion: str = descripcion
        self.monto: float = monto
        self.categoria: str = categoria

    def es_ingreso(self) -> bool:
        #Devuelve True si la transacción es un ingreso.
        return self.monto > 0


# Lógica de Negocio
class ILogicaFinanciera:
    #Interfaz para la lógica financiera.
    #Permite aplicar inversión de dependencias (DIP).

    def agregar_transaccion(self, fecha: datetime.date, descripcion: str, monto: float, categoria: str) -> bool:
        raise NotImplementedError

    def obtener_resumen_por_categoria(self) -> str:
        raise NotImplementedError

    def analisis_predictivo(self, dias_a_predecir: int = 30) -> Tuple[Optional[plt.Figure], Optional[str]]:
        raise NotImplementedError


class LogicaFinanciera(ILogicaFinanciera):
    
    #Implementación concreta de la lógica financiera.
    #Maneja transacciones y análisis de datos.

    def __init__(self):
        self.transacciones: List[Transaccion] = []
        self._cargar_datos_ejemplo()

    def _cargar_datos_ejemplo(self) -> None:
        #Carga datos de ejemplo para la aplicación.
        fecha_base = datetime.date.today() - datetime.timedelta(days=90)
        for i in range(3):
            desplazamiento_mes = i * 30
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 1), "Salario Mensual", 2500, "Ingreso")
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 2), "Alquiler", -1200, "Vivienda")
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 5), "Supermercado", -150 - np.random.rand() * 20, "Alimentación")
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 10), "Transporte", -50 - np.random.rand() * 10, "Transporte")
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 15), "Restaurante", -75 - np.random.rand() * 30, "Ocio")

    def agregar_transaccion(self, fecha: datetime.date, descripcion: str, monto: float, categoria: str) -> bool:
        # Añade una transacción a la lista.
        transaccion = Transaccion(fecha, descripcion, monto, categoria)
        self.transacciones.append(transaccion)
        self.transacciones.sort(key=lambda x: x.fecha, reverse=True)
        return True

    def obtener_resumen_por_categoria(self) -> str:
        # Genera un resumen de ingresos, gastos y saldo total.
        if not self.transacciones:
            return "No hay transacciones para resumir."

        resumen: Dict[str, float] = defaultdict(float)
        ingreso_total: float = 0.0
        gasto_total: float = 0.0

        for transaccion in self.transacciones:
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

    def analisis_predictivo(self, dias_a_predecir: int = 30) -> Tuple[Optional[plt.Figure], Optional[str]]:
        # Genera un análisis predictivo de gastos mediante regresión lineal.
        if len(self.transacciones) < 10:
            return None, "No hay suficientes datos para realizar un análisis predictivo."

        dataframe = pd.DataFrame([vars(t) for t in self.transacciones])
        dataframe["fecha"] = pd.to_datetime(dataframe["fecha"])

        gastos = dataframe[dataframe["monto"] < 0].copy()
        if gastos.empty:
            return None, "No hay gastos registrados para el análisis predictivo."

        gastos["monto"] = gastos["monto"].abs()
        gastos_diarios = gastos.set_index("fecha").resample("D")["monto"].sum().reset_index()
        gastos_diarios = gastos_diarios[gastos_diarios["monto"] > 0]

        if len(gastos_diarios) < 2:
            return None, "No hay suficientes días con gastos para la predicción."

        gastos_diarios["dias_desde_inicio"] = (gastos_diarios["fecha"] - gastos_diarios["fecha"].min()).dt.days
        X, y = gastos_diarios[["dias_desde_inicio"]], gastos_diarios["monto"]

        modelo = LinearRegression()
        modelo.fit(X, y)

        ultimo_dia = X["dias_desde_inicio"].max()
        dias_futuros = np.array(range(ultimo_dia + 1, ultimo_dia + 1 + dias_a_predecir)).reshape(-1, 1)
        gastos_predichos = modelo.predict(dias_futuros)
        gastos_predichos[gastos_predichos < 0] = 0

        figura, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(X, y, color="blue", label="Gastos Históricos", alpha=0.6)
        ax.plot(X, modelo.predict(X), color="green", linewidth=2, label="Tendencia")
        fechas_futuras = pd.to_datetime(gastos_diarios["fecha"].min()) + pd.to_timedelta(dias_futuros.flatten(), unit="d")
        ax.plot(fechas_futuras, gastos_predichos, color="red", linestyle="--", linewidth=2, label=f"Predicción {dias_a_predecir} días")

        ax.set_title(f"Análisis Predictivo de Gastos\nPredicción Total: ${gastos_predichos.sum():,.2f}", fontsize=14)
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Monto de Gasto ($)")
        ax.legend()
        figura.autofmt_xdate()
        plt.tight_layout()

        return figura, None


# Interfaz Gráfica 
class AppGraficaFinanzas(tk.Tk):
    
    # Interfaz gráfica de la aplicación de finanzas personales.

    def __init__(self, servicio: ILogicaFinanciera):
        super().__init__()
        self.title("Ahorra Pro")
        self.geometry("1000x600")

        self.servicio = servicio
        self._configurar_estilos()
        self._crear_widgets()
        self._actualizar_vista_transacciones()

    def _configurar_estilos(self) -> None:
        # Configura los estilos visuales. 
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=25, font=("Arial", 10))
        estilo.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        estilo.map("TButton", background=[("active", "#A9A9A9")])

    def _crear_widgets(self) -> None:
        # Crea y organiza los widgets en la interfaz.
        marco_principal = ttk.Frame(self, padding="10")
        marco_principal.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo: formulario y acciones
        marco_izquierdo = ttk.Frame(marco_principal, padding="10", relief="solid", borderwidth=1)
        marco_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self._crear_formulario(marco_izquierdo)
        self._crear_acciones(marco_izquierdo)
        self._crear_resumen(marco_izquierdo)

        # Panel derecho: tabla de transacciones
        self._crear_tabla(marco_principal)

    def _crear_formulario(self, parent: ttk.Frame) -> None:
        # Crea el formulario de ingreso de transacciones.
        marco_formulario = ttk.LabelFrame(parent, text="Añadir Transacción", padding="10")
        marco_formulario.pack(fill=tk.X, pady=(0, 10))

        campos = [
            ("Fecha (AAAA-MM-DD):", "entrada_fecha", datetime.date.today().strftime("%Y-%m-%d")),
            ("Descripción:", "entrada_descripcion", ""),
            ("Monto (negativo = gasto):", "entrada_monto", ""),
            ("Categoría:", "entrada_categoria", ""),
        ]

        for idx, (label, attr, default) in enumerate(campos):
            ttk.Label(marco_formulario, text=label).grid(row=idx * 2, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(marco_formulario, width=30)
            entry.insert(0, default)
            entry.grid(row=idx * 2 + 1, column=0, sticky=tk.W, pady=2)
            setattr(self, attr, entry)

        ttk.Button(marco_formulario, text="Añadir", command=self._agregar_transaccion).grid(row=8, column=0, sticky=tk.EW, pady=10)

    def _crear_acciones(self, parent: ttk.Frame) -> None:
        # Crea botones de acciones adicionales.
        marco_acciones = ttk.LabelFrame(parent, text="Acciones", padding="10")
        marco_acciones.pack(fill=tk.X, pady=10)

        ttk.Button(marco_acciones, text="Ver Resumen", command=self._mostrar_resumen).pack(fill=tk.X, pady=5)
        ttk.Button(marco_acciones, text="Análisis Predictivo", command=self._ejecutar_prediccion).pack(fill=tk.X, pady=5)

    def _crear_resumen(self, parent: ttk.Frame) -> None:
        # Crea el panel para mostrar el resumen financiero.
        marco_resumen = ttk.LabelFrame(parent, text="Resumen", padding="10")
        marco_resumen.pack(fill=tk.BOTH, expand=True)

        self.texto_resumen = tk.Text(marco_resumen, wrap=tk.WORD, height=10, width=35, font=("Courier", 9))
        self.texto_resumen.pack(fill=tk.BOTH, expand=True)
        self.texto_resumen.insert(tk.END, "Presiona 'Ver Resumen' para ver los datos.")
        self.texto_resumen.config(state=tk.DISABLED)

    def _crear_tabla(self, parent: ttk.Frame) -> None:
        # Crea la tabla que lista las transacciones.
        marco_derecho = ttk.Frame(parent)
        marco_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columnas = ("Fecha", "Descripción", "Categoría", "Monto")
        self.arbol = ttk.Treeview(marco_derecho, columns=columnas, show="headings", selectmode="browse")

        for col in columnas:
            self.arbol.heading(col, text=col)
        self.arbol.column("Fecha", width=100, anchor=tk.CENTER)
        self.arbol.column("Descripción", width=250)
        self.arbol.column("Categoría", width=120)
        self.arbol.column("Monto", width=100, anchor=tk.E)

        self.arbol.tag_configure("ingreso", foreground="green")
        self.arbol.tag_configure("gasto", foreground="red")

        barra_scroll = ttk.Scrollbar(marco_derecho, orient=tk.VERTICAL, command=self.arbol.yview)
        self.arbol.configure(yscroll=barra_scroll.set)

        barra_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _agregar_transaccion(self) -> None:
        # Obtiene los datos del formulario y añade la transacción.
        try:
            fecha = datetime.datetime.strptime(self.entrada_fecha.get(), "%Y-%m-%d").date()
            descripcion = self.entrada_descripcion.get().strip()
            monto = float(self.entrada_monto.get())
            categoria = self.entrada_categoria.get().strip()

            if not descripcion or not categoria:
                messagebox.showerror("Error", "La descripción y la categoría son obligatorias.")
                return

            self.servicio.agregar_transaccion(fecha, descripcion, monto, categoria)
            self._actualizar_vista_transacciones()

            self.entrada_descripcion.delete(0, tk.END)
            self.entrada_monto.delete(0, tk.END)
            self.entrada_categoria.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error de Formato", "Introduce fecha válida (AAAA-MM-DD) y monto numérico.")

    def _actualizar_vista_transacciones(self) -> None:
        # Recarga la tabla de transacciones.
        for item in self.arbol.get_children():
            self.arbol.delete(item)

        for t in self.servicio.transacciones:
            monto_texto = f"${t.monto:,.2f}"
            etiqueta = "ingreso" if t.es_ingreso() else "gasto"
            self.arbol.insert("", tk.END, values=(t.fecha, t.descripcion, t.categoria, monto_texto), tags=(etiqueta,))

    def _mostrar_resumen(self) -> None:
        # Muestra el resumen en el panel lateral. 
        texto = self.servicio.obtener_resumen_por_categoria()
        self.texto_resumen.config(state=tk.NORMAL)
        self.texto_resumen.delete("1.0", tk.END)
        self.texto_resumen.insert(tk.END, texto)
        self.texto_resumen.config(state=tk.DISABLED)

    def _ejecutar_prediccion(self) -> None:
        # Genera un gráfico predictivo y lo muestra en una ventana nueva.
        figura, mensaje = self.servicio.analisis_predictivo()

        if mensaje:
            messagebox.showinfo("Análisis Predictivo", mensaje)
            return

        ventana = tk.Toplevel(self)
        ventana.title("Gráfico Predictivo")
        ventana.geometry("800x600")

        lienzo = FigureCanvasTkAgg(figura, master=ventana)
        lienzo.draw()
        lienzo.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Punto de Entrada 
if __name__ == "__main__":
    servicio = LogicaFinanciera()
    app = AppGraficaFinanzas(servicio)
    app.mainloop()
