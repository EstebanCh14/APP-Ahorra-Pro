# ui/AppGraficaFinanzas/components/app.py
import datetime
import tkinter as tk
from tkinter import ttk, messagebox

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from common.utils import Observer
from gateway.AppGraficaFinanzas.main import FinanzasGateway


class AppGraficaFinanzas(tk.Tk, Observer):
    """
    Interfaz gráfica de la aplicación de finanzas personales.
    Actúa como Observer (se suscribe a LogicaFinanciera) y
    usa el Gateway como Mediator para hablar con los microservicios.
    """
    def __init__(self, gateway: FinanzasGateway):
        super().__init__()
        self.title("Ahorra Pro")
        self.geometry("1000x600")

        self.gateway = gateway

        # La UI se suscribe a los cambios de transacciones
        self.gateway.logica_financiera.attach(self)

        self._configurar_estilos()
        self._crear_widgets()
        self._actualizar_vista_transacciones()

    # --- Métodos del Observer ---
    def update(self, event: str, data=None) -> None:
        """
        Método invocado cuando el Subject (LogicaFinanciera) notifica cambios.
        """
        if event == "TRANSACCION_AGREGADA":
            self._actualizar_vista_transacciones()
            # Podríamos refrescar el resumen automáticamente si quieres:
            # self._mostrar_resumen()

    # --- Configuración de estilos ---
    def _configurar_estilos(self) -> None:
        estilo = ttk.Style(self)
        estilo.theme_use("clam")
        estilo.configure("Treeview", rowheight=25, font=("Arial", 10))
        estilo.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        estilo.map("TButton", background=[("active", "#A9A9A9")])

    def _crear_widgets(self) -> None:
        marco_principal = ttk.Frame(self, padding="10")
        marco_principal.pack(fill=tk.BOTH, expand=True)

        # Panel izquierdo
        marco_izquierdo = ttk.Frame(marco_principal, padding="10",
                                    relief="solid", borderwidth=1)
        marco_izquierdo.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self._crear_formulario(marco_izquierdo)
        self._crear_acciones(marco_izquierdo)
        self._crear_resumen(marco_izquierdo)

        # Panel derecho
        self._crear_tabla(marco_principal)

    def _crear_formulario(self, parent: ttk.Frame) -> None:
        marco_formulario = ttk.LabelFrame(parent, text="Añadir Transacción", padding="10")
        marco_formulario.pack(fill=tk.X, pady=(0, 10))

        campos = [
            ("Fecha (AAAA-MM-DD):", "entrada_fecha",
            datetime.date.today().strftime("%Y-%m-%d")),
            ("Descripción:", "entrada_descripcion", ""),
            ("Monto (negativo = gasto):", "entrada_monto", ""),
            ("Categoría:", "entrada_categoria", ""),
        ]

        for idx, (label, attr, default) in enumerate(campos):
            ttk.Label(marco_formulario, text=label).grid(row=idx * 2,
                                                        column=0,
                                                        sticky=tk.W,
                                                        pady=2)
            entry = ttk.Entry(marco_formulario, width=30)
            entry.insert(0, default)
            entry.grid(row=idx * 2 + 1, column=0, sticky=tk.W, pady=2)
            setattr(self, attr, entry)

        ttk.Button(marco_formulario, text="Añadir",
                command=self._agregar_transaccion).grid(
            row=8, column=0, sticky=tk.EW, pady=10
        )

    def _crear_acciones(self, parent: ttk.Frame) -> None:
        marco_acciones = ttk.LabelFrame(parent, text="Acciones", padding="10")
        marco_acciones.pack(fill=tk.X, pady=10)

        ttk.Button(marco_acciones, text="Ver Resumen",
                command=self._mostrar_resumen).pack(fill=tk.X, pady=5)
        ttk.Button(marco_acciones, text="Análisis Predictivo",
                command=self._ejecutar_prediccion).pack(fill=tk.X, pady=5)

    def _crear_resumen(self, parent: ttk.Frame) -> None:
        marco_resumen = ttk.LabelFrame(parent, text="Resumen", padding="10")
        marco_resumen.pack(fill=tk.BOTH, expand=True)

        self.texto_resumen = tk.Text(marco_resumen,
                                    wrap=tk.WORD,
                                    height=10,
                                    width=35,
                                    font=("Courier", 9))
        self.texto_resumen.pack(fill=tk.BOTH, expand=True)
        self.texto_resumen.insert(tk.END, "Presiona 'Ver Resumen' para ver los datos.")
        self.texto_resumen.config(state=tk.DISABLED)

    def _crear_tabla(self, parent: ttk.Frame) -> None:
        marco_derecho = ttk.Frame(parent)
        marco_derecho.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columnas = ("Fecha", "Descripción", "Categoría", "Monto")
        self.arbol = ttk.Treeview(marco_derecho,
                                columns=columnas,
                                show="headings",
                                selectmode="browse")

        for col in columnas:
            self.arbol.heading(col, text=col)
        self.arbol.column("Fecha", width=100, anchor=tk.CENTER)
        self.arbol.column("Descripción", width=250)
        self.arbol.column("Categoría", width=120)
        self.arbol.column("Monto", width=100, anchor=tk.E)

        self.arbol.tag_configure("ingreso", foreground="green")
        self.arbol.tag_configure("gasto", foreground="red")

        barra_scroll = ttk.Scrollbar(marco_derecho,
                                    orient=tk.VERTICAL,
                                    command=self.arbol.yview)
        self.arbol.configure(yscroll=barra_scroll.set)

        barra_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.arbol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # --- Lógica conectada al Gateway ---

    def _agregar_transaccion(self) -> None:
        try:
            fecha = datetime.datetime.strptime(
                self.entrada_fecha.get(), "%Y-%m-%d"
            ).date()
            descripcion = self.entrada_descripcion.get().strip()
            monto = float(self.entrada_monto.get())
            categoria = self.entrada_categoria.get().strip()

            if not descripcion or not categoria:
                messagebox.showerror(
                    "Error",
                    "La descripción y la categoría son obligatorias."
                )
                return

            self.gateway.agregar_transaccion(fecha, descripcion, monto, categoria)

            # Limpiar campos del formulario
            self.entrada_descripcion.delete(0, tk.END)
            self.entrada_monto.delete(0, tk.END)
            self.entrada_categoria.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Error de Formato",
                "Introduce fecha válida (AAAA-MM-DD) y monto numérico."
            )

    def _actualizar_vista_transacciones(self) -> None:
        for item in self.arbol.get_children():
            self.arbol.delete(item)

        for t in self.gateway.obtener_transacciones():
            monto_texto = f"${t.monto:,.2f}"
            etiqueta = "ingreso" if t.es_ingreso() else "gasto"
            self.arbol.insert(
                "",
                tk.END,
                values=(t.fecha, t.descripcion, t.categoria, monto_texto),
                tags=(etiqueta,)
            )

    def _mostrar_resumen(self) -> None:
        texto = self.gateway.obtener_resumen_por_categoria()
        self.texto_resumen.config(state=tk.NORMAL)
        self.texto_resumen.delete("1.0", tk.END)
        self.texto_resumen.insert(tk.END, texto)
        self.texto_resumen.config(state=tk.DISABLED)

    def _ejecutar_prediccion(self) -> None:
        figura, mensaje = self.gateway.analisis_predictivo()

        if mensaje:
            messagebox.showinfo("Análisis Predictivo", mensaje)
            return

        ventana = tk.Toplevel(self)
        ventana.title("Gráfico Predictivo")
        ventana.geometry("800x600")

        lienzo = FigureCanvasTkAgg(figura, master=ventana)
        lienzo.draw()
        lienzo.get_tk_widget().pack(fill=tk.BOTH, expand=True)
