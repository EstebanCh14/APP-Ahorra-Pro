# ui/AppGraficaFinanzas/Main.py
from gateway.AppGraficaFinanzas.main import crear_gateway
from ui.AppGraficaFinanzas.components.app import AppGraficaFinanzas


def main():
    gateway = crear_gateway()
    app = AppGraficaFinanzas(gateway)
    app.mainloop()


if __name__ == "__main__":
    main()
