# AhorraPro 2.0 — Arquitectura en Microservicios

Aplicación de finanzas personales desarrollada en Python, que permite gestionar ingresos, gastos y analizar el comportamiento financiero mediante predicciones inteligentes.  
Construida bajo una arquitectura modular y orientada a microservicios, integra los patrones de diseño Adapter, Factory Method y Observer, garantizando un sistema flexible, mantenible y escalable.

---

## Estructura del Proyecto

AhorraPro/
│
├── common/ # Interfaces, tipos y clases base compartidas
│ ├── models/ # Entidades de dominio (Transacción, Reporte, etc.)
│ ├── observer.py # Implementación del patrón Observer
│ └── utils.py # Funciones y utilidades comunes
│
├── servicio_transaccion/ # Módulo de manejo de transacciones (Factory Method)
│ ├── TransactionFactory.py
│ ├── TransactionRepository.py
│ ├── TransactionServiceImpl.py
│ └── main.py
│
├── servicio_reporte/ # Generación y control de reportes financieros
│ ├── GeneradorReporte.py
│ ├── ControladorResumen.py
│ └── main.py
│
├── servicio_prediccion/ # Predicción de gastos usando scikit-learn (Adapter)
│ ├── SklearnAdapter.py
│ ├── ServicioPrediccion.py
│ └── main.py
│
├── gateway/ # Orquestador principal (Observer)
│ ├── routes_transacciones.py
│ ├── routes_reportes.py
│ ├── routes_predicciones.py
│ └── main.py
│
├── ui/ # Interfaz gráfica del usuario (Tkinter)
│ ├── AppGraficaFinanzas.py
│ ├── components/
│ ├── assets/
│ └── main.py
│
├── run_app.py # Lanzador universal del proyecto
└── requirements.txt # Dependencias del sistema

---

## Patrones de Diseño Implementados

### **Adapter Pattern**
Ubicación: `servicio_prediccion/SklearnAdapter.py`  
Permite adaptar modelos de `scikit-learn` al formato interno de AhorraPro, manteniendo la independencia entre el motor de predicción y la lógica del sistema.

---

### **Factory Method**
Ubicación: `servicio_transaccion/TransactionFactory.py`  
Centraliza la creación de objetos `Transaccion` (ingreso/gasto) sin acoplar la lógica de instanciación a la capa de presentación.

---

### **Observer Pattern**
Ubicación: `gateway/`  
Permite que la interfaz gráfica se suscriba a los cambios de datos en el sistema.  
Cuando una transacción se registra o modifica, la vista se actualiza automáticamente.

---

## Requisitos del Sistema

- **Python 3.10 o superior**
- **Tkinter** (incluido por defecto en Python)
- Librerías externas:
  ```bash
  numpy
  pandas
  matplotlib
  scikit-learn
Instalación rápida de dependencias
python -m pip install -r requirements.txt

Ejecución del Proyecto
Desde la carpeta raíz del proyecto:

python -m ui.AppGraficaFinanzas.main

O si usas la versión de Python instalada desde Microsoft Store:

py -m ui.AppGraficaFinanzas.main

Ejemplo de ruta en Windows:
C:\Users\<usuario>\OneDrive\Desktop\AhorraPro\AhorraPro

Funcionalidades Principales
- Registro de ingresos y gastos
- Resumen financiero por categorías
- Cálculo automático del saldo total
- Visualización gráfica de datos con Matplotlib
- Predicción de gastos mediante Regresión Lineal
- Arquitectura basada en microservicios
- Interfaz gráfica interactiva y responsiva (Tkinter)

Equipo de Desarrollo
Integrante	Rol
Camila Vélez Posada	Desarrolladora principal / Arquitectura de microservicios
Juan Esteban Chica Masmela	QA y pruebas funcionales / Documentación técnica
José Daniel Ramírez Urrego	Soporte técnico / Integración de servicios
Harly Córdoba Cano	Análisis de datos / Optimización del módulo predictivo

Detalle Técnico
Componente	Tecnología
Frontend (UI)	Tkinter (Python GUI)
Backend	Microservicios independientes (Gateway + Servicios)
Modelo Predictivo	LinearRegression — scikit-learn
Reportes	Generados en tiempo real (Servicio de Reporte)
Persistencia	En memoria (listas Python) — extensible a SQL o NoSQL
Arquitectura	Microservicios + Patrones de Diseño Clásicos

Inspiración Arquitectónica
Este proyecto evoluciona desde una versión monolítica anterior, refactorizada para aplicar principios SOLID y una arquitectura basada en microservicios, buscando mejorar la separación de responsabilidades, escalabilidad y mantenibilidad del código.

Licencia
Proyecto académico — uso libre con fines educativos.
Desarrollado con ❤️ por nuestro equipo de trabajo.
