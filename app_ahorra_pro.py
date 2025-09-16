import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
from sklearn.linear_model import LinearRegression

# --- Clase de Lógica de Negocio ---
class LogicaFinanciera:
    """
    Maneja todo el procesamiento de datos y la lógica financiera,
    de forma completamente separada de la interfaz gráfica.
    """
    def __init__(self):
        self.transacciones = []
        self._cargar_datos_ejemplo()

    def _cargar_datos_ejemplo(self):
        """Carga datos de ejemplo para demostrar la funcionalidad de la aplicación."""
        fecha_base = datetime.date.today() - datetime.timedelta(days=90)
        for i in range(3):
            desplazamiento_mes = i * 30
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 1), 'Salario Mensual', 2500, 'Ingreso')
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 2), 'Alquiler', -1200, 'Vivienda')
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 5), 'Supermercado', -150 - np.random.rand() * 20, 'Alimentación')
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 10), 'Transporte', -50 - np.random.rand() * 10, 'Transporte')
            self.agregar_transaccion(fecha_base + datetime.timedelta(days=desplazamiento_mes + 15), 'Restaurante', -75 - np.random.rand() * 30, 'Ocio')

    def agregar_transaccion(self, fecha, descripcion, monto, categoria):
        """Añade una nueva transacción a la lista."""
        transaccion = {
            "fecha": fecha,
            "descripcion": descripcion,
            "monto": monto,
            "categoria": categoria,
        }
        self.transacciones.append(transaccion)
        self.transacciones.sort(key=lambda x: x['fecha'], reverse=True)
        return True

    def obtener_resumen_por_categoria(self):
        """Calcula y devuelve un string con el resumen de finanzas."""
        if not self.transacciones:
            return "No hay transacciones para resumir."

        resumen = defaultdict(float)
        ingreso_total = 0.0
        gasto_total = 0.0

        for transaccion in self.transacciones:
            if transaccion['monto'] < 0:
                resumen[transaccion['categoria']] += transaccion['monto']
                gasto_total += transaccion['monto']
            else:
                ingreso_total += transaccion['monto']

        saldo = ingreso_total + gasto_total
        
        texto_resumen = "--- Resumen de Gastos por Categoría ---\n"
        if not resumen:
            texto_resumen += "No hay gastos registrados.\n"
        else:
            for categoria, total in sorted(resumen.items(), key=lambda item: item[1]):
                texto_resumen += f"{categoria:<20}: ${total:,.2f}\n"
        
        texto_resumen += "\n--- Resumen General ---\n"
        texto_resumen += f"Ingresos Totales: ${ingreso_total:,.2f}\n"
        texto_resumen += f"Gastos Totales:   ${gasto_total:,.2f}\n"
        texto_resumen += f"Saldo General:    ${saldo:,.2f}\n"
        
        return texto_resumen

    def analisis_predictivo(self, dias_a_predecir=30):
        """Realiza un análisis predictivo y devuelve la figura del gráfico."""
        if len(self.transacciones) < 10:
            return None, "No hay suficientes datos para realizar un análisis predictivo."

        dataframe = pd.DataFrame(self.transacciones)
        dataframe['fecha'] = pd.to_datetime(dataframe['fecha'])
        
        gastos = dataframe[dataframe['monto'] < 0].copy()
        if gastos.empty:
            return None, "No hay gastos registrados para el análisis predictivo."
            
        gastos['monto'] = gastos['monto'].abs()
        gastos_diarios = gastos.set_index('fecha').resample('D')['monto'].sum().reset_index()
        gastos_diarios = gastos_diarios[gastos_diarios['monto'] > 0]

        if len(gastos_diarios) < 2:
            return None, "No hay suficientes días con gastos para la predicción."

        gastos_diarios['dias_desde_inicio'] = (gastos_diarios['fecha'] - gastos_diarios['fecha'].min()).dt.days
        X = gastos_diarios[['dias_desde_inicio']]
        y = gastos_diarios['monto']

        modelo = LinearRegression()
        modelo.fit(X, y)

        ultimo_dia = X['dias_desde_inicio'].max()
        dias_futuros = np.array(range(ultimo_dia + 1, ultimo_dia + 1 + dias_a_predecir)).reshape(-1, 1)
        gastos_predichos = modelo.predict(dias_futuros)
        gastos_predichos[gastos_predichos < 0] = 0

        figura, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(X, y, color='blue', label='Gastos Diarios Históricos', alpha=0.6)
        ax.plot(X, modelo.predict(X), color='green', linewidth=2, label='Línea de Tendencia')
        fechas_futuras = pd.to_datetime(gastos_diarios['fecha'].min()) + pd.to_timedelta(dias_futuros.flatten(), unit='d')
        ax.plot(fechas_futuras, gastos_predichos, color='red', linestyle='--', linewidth=2, label=f'Predicción a {dias_a_predecir} días')
        
        total_predicho = gastos_predichos.sum()
        ax.set_title(f'Análisis Predictivo de Gastos\nPredicción Total: ${total_predicho:,.2f}', fontsize=14)
        ax.set_xlabel('Fecha', fontsize=10)
        ax.set_ylabel('Monto de Gasto ($)', fontsize=10)
        ax.legend()
        figura.autofmt_xdate()
        plt.tight_layout()
        
        return figura, None

# --- Clase de la Interfaz Gráfica ---
class AppGraficaFinanzas(tk.Tk):
    """
    Maneja todos los componentes de la interfaz gráfica y la interacción del usuario.
    """
    def __init__(self):
        super().__init__()
        self.title("Ahorra Pro")
        self.geometry("1000x600")

        self.logica = LogicaFinanciera()

        self.estilo = ttk.Style(self)
        self.estilo.theme_use("clam")
        self.estilo.configure("Treeview", rowheight=25, font=("Arial", 10))
        self.estilo.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        self.estilo.map('TButton', background=[('active', '#A9A9A9')])

        self.crear_widgets()
        self.actualizar_vista_transacciones()

    def crear_widgets(self):
        """Crea y posiciona todos los elementos gráficos en la ventana."""
        marco_principal = ttk.Frame(self, padding="10")
        marco_principal.pack(fill=tk.BOTH, expand=True)

        marco_izquierdo = ttk.Frame(marco_principal, padding="10", relief="solid", borderwidth=1)
        marco_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        marco_formulario = ttk.LabelFrame(marco_izquierdo, text="Añadir Nueva Transacción", padding="10")
        marco_formulario.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(marco_formulario, text="Fecha (AAAA-MM-DD):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entrada_fecha = ttk.Entry(marco_formulario, width=30)
        self.entrada_fecha.grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entrada_fecha.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        ttk.Label(marco_formulario, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entrada_descripcion = ttk.Entry(marco_formulario, width=30)
        self.entrada_descripcion.grid(row=3, column=0, sticky=tk.W, pady=2)

        ttk.Label(marco_formulario, text="Monto (negativo para gastos):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.entrada_monto = ttk.Entry(marco_formulario, width=30)
        self.entrada_monto.grid(row=5, column=0, sticky=tk.W, pady=2)

        ttk.Label(marco_formulario, text="Categoría:").grid(row=6, column=0, sticky=tk.W, pady=2)
        self.entrada_categoria = ttk.Entry(marco_formulario, width=30)
        self.entrada_categoria.grid(row=7, column=0, sticky=tk.W, pady=2)
        
        boton_agregar = ttk.Button(marco_formulario, text="Añadir Transacción", command=self.agregar_transaccion)
        boton_agregar.grid(row=8, column=0, sticky=tk.EW, pady=10)

        marco_acciones = ttk.LabelFrame(marco_izquierdo, text="Acciones", padding="10")
        marco_acciones.pack(fill=tk.X, pady=10)
        
        boton_resumen = ttk.Button(marco_acciones, text="Ver Resumen por Categoría", command=self.mostrar_resumen)
        boton_resumen.pack(fill=tk.X, pady=5)
        
        boton_predecir = ttk.Button(marco_acciones, text="Análisis Predictivo de Gastos", command=self.ejecutar_prediccion)
        boton_predecir.pack(fill=tk.X, pady=5)

        marco_visor_resumen = ttk.LabelFrame(marco_izquierdo, text="Resumen", padding="10")
        marco_visor_resumen.pack(fill=tk.BOTH, expand=True)

        self.texto_resumen = tk.Text(marco_visor_resumen, wrap=tk.WORD, height=10, width=35, font=("Courier", 9))
        self.texto_resumen.pack(fill=tk.BOTH, expand=True)
        self.texto_resumen.insert(tk.END, "Presiona 'Ver Resumen' para ver los datos.")
        self.texto_resumen.config(state=tk.DISABLED)
        
        marco_derecho = ttk.Frame(marco_principal)
        marco_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        columnas = ('Fecha', 'Descripción', 'Categoría', 'Monto')
        self.arbol = ttk.Treeview(marco_derecho, columns=columnas, show='headings', selectmode="browse")
        
        for col in columnas:
            self.arbol.heading(col, text=col)
        self.arbol.column("Fecha", width=100, anchor=tk.CENTER)
        self.arbol.column("Descripción", width=250)
        self.arbol.column("Categoría", width=120)
        self.arbol.column("Monto", width=100, anchor=tk.E)

        self.arbol.tag_configure('ingreso', foreground='green')
        self.arbol.tag_configure('gasto', foreground='red')

        barra_desplazamiento = ttk.Scrollbar(marco_derecho, orient=tk.VERTICAL, command=self.arbol.yview)
        self.arbol.configure(yscroll=barra_desplazamiento.set)
        
        barra_desplazamiento.pack(side=tk.RIGHT, fill=tk.Y)
        self.arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def agregar_transaccion(self):
        """Toma los datos de los campos de entrada y los añade a la lógica."""
        try:
            fecha_texto = self.entrada_fecha.get()
            fecha = datetime.datetime.strptime(fecha_texto, "%Y-%m-%d").date()
            descripcion = self.entrada_descripcion.get()
            monto = float(self.entrada_monto.get())
            categoria = self.entrada_categoria.get()

            if not descripcion or not categoria:
                messagebox.showerror("Error de Entrada", "La descripción y la categoría no pueden estar vacías.")
                return

            self.logica.agregar_transaccion(fecha, descripcion, monto, categoria)
            self.actualizar_vista_transacciones()
            
            self.entrada_descripcion.delete(0, tk.END)
            self.entrada_monto.delete(0, tk.END)
            self.entrada_categoria.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Error de Formato", "Por favor, introduce una fecha válida (AAAA-MM-DD) y un monto numérico.")

    def actualizar_vista_transacciones(self):
        """Limpia y vuelve a poblar la tabla con las transacciones actuales."""
        for i in self.arbol.get_children():
            self.arbol.delete(i)
        
        for transaccion in self.logica.transacciones:
            monto_texto = f"${transaccion['monto']:,.2f}"
            etiqueta = 'ingreso' if transaccion['monto'] > 0 else 'gasto'
            self.arbol.insert('', tk.END, values=(transaccion['fecha'], transaccion['descripcion'], transaccion['categoria'], monto_texto), tags=(etiqueta,))

    def mostrar_resumen(self):
        """Obtiene el resumen de la lógica y lo muestra en el cuadro de texto."""
        texto_resumen = self.logica.obtener_resumen_por_categoria()
        self.texto_resumen.config(state=tk.NORMAL)
        self.texto_resumen.delete('1.0', tk.END)
        self.texto_resumen.insert(tk.END, texto_resumen)
        self.texto_resumen.config(state=tk.DISABLED)

    def ejecutar_prediccion(self):
        """Pide a la lógica que genere un gráfico y lo muestra en una nueva ventana."""
        figura, mensaje_error = self.logica.analisis_predictivo()
        
        if mensaje_error:
            messagebox.showinfo("Análisis Predictivo", mensaje_error)
            return

        ventana_grafico = tk.Toplevel(self)
        ventana_grafico.title("Gráfico de Análisis Predictivo")
        ventana_grafico.geometry("800x600")

        lienzo = FigureCanvasTkAgg(figura, master=ventana_grafico)
        lienzo.draw()
        lienzo.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# --- Punto de Entrada del Script ---
# Este bloque es crucial. Sin él, el programa se ejecuta y se cierra.
if __name__ == "__main__":
    app = AppGraficaFinanzas()
    app.mainloop() # Esta línea mantiene la ventana abierta