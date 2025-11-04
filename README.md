# 💰 AhorraPro 2.0 — Arquitectura en Microservicios
Aplicación de **finanzas personales** desarrollada en **Python**, que permite gestionar ingresos, gastos y realizar análisis predictivos de comportamiento financiero.  
Construida bajo una **arquitectura modular y orientada a microservicios**, integra patrones de diseño **Adapter**, **Factory Method** y **Observer** para lograr un sistema flexible, mantenible y extensible.
---
## 🏗️ Estructura del Proyecto
AhorraPro/
│
├── common/ # Interfaces, tipos y clases base
├── gateway/ # Orquestador principal (Observer)
│ └── AppGraficaFinanzas/ # Gateway entre UI y lógica
│
├── servicio_transaccion/ # Lógica de transacciones (Factory Method)
├── servicio_reporte/ # Generación de reportes financieros
├── servicio_prediccion/ # Predicción de gastos con scikit-learn (Adapter)
│
├── ui/
│ └── AppGraficaFinanzas/ # Interfaz gráfica con Tkinter
│ ├── components/
│ ├── assets/
│ └── Main.py # Punto de entrada de la UI
│
├── run_app.py # Lanzador universal del proyecto
└── requirements.txt # Dependencias
---




## 🧩 Patrones de Diseño Implementados
### 🧱 **Adapter Pattern**
Implementado en `servicio_prediccion/SklearnAdapter.py`, permite adaptar modelos de `scikit-learn` al formato de predicciones de AhorraPro sin modificar la lógica central.
### 🏭 **Factory Method**
Aplicado en `servicio_transaccion/TransactionFactory.py` para crear objetos `Transaccion` según su tipo (ingreso o gasto), encapsulando la lógica de creación.
### 👁️ **Observer Pattern**
Presente en `gateway/`, donde la interfaz (`UI`) se suscribe a los cambios de datos en la capa de negocio, actualizando automáticamente la vista cuando se agrega o modifica una transacción.
---
## ⚙️ Requisitos del Sistema
- **Python 3.10 o superior**
- **Tkinter** (incluido con Python)
- Librerías externas:
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `scikit-learn`
Instalación rápida de dependencias:
```bash
python -m pip install -r requirements.txt



🚀 Ejecución del Proyecto
Desde la carpeta raíz del proyecto (por ejemplo:
C:\Users\Camila\OneDrive\Desktop\AhorraPro (2)\AhorraPro
o
C:\Users\juane\OneDrive\Desktop\AhorraPro):
python -m ui.AppGraficaFinanzas.Main
🪟 Si tienes la versión de Python instalada desde Microsoft Store (como Juan):
py -m ui.AppGraficaFinanzas.Main
🧠 Funcionalidades Principales
✅ Registro de ingresos y gastos
✅ Resumen financiero por categorías
✅ Cálculo de saldo total
✅ Gráficos y visualización de datos con Matplotlib
✅ Análisis predictivo de gastos (Regresión Lineal)
✅ Arquitectura basada en microservicios
✅ Interfaz gráfica interactiva con Tkinter
👥 Integrantes del Proyecto
Nombre	Rol
Camila Vélez Posada	Desarrolladora principal / Arquitectura de microservicios
Juan Esteban Chica Masmela	QA y pruebas funcionales / Documentación técnica
José Daniel Ramírez Urrego	Soporte técnico / Integración de servicios y pruebas
Harly Córdoba Cano	Análisis de datos / Optimización del módulo predictivo




🧩 Detalle Técnico
•	Frontend: Tkinter (Python GUI)
•	Backend: Microservicios Python (Gateway + Servicios independientes)
•	Modelo predictivo: LinearRegression (Scikit-learn)
•	Reportes: Generados en tiempo real (Servicio de Reporte)
•	Persistencia: En memoria (listas Python) — extensible a base de datos SQL o NoSQL
