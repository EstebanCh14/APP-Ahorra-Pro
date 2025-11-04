# common/utils.py
from typing import Protocol, List, Optional, Any

class Observer(Protocol):
    """
    Observador genérico para el patrón Observer.
    """
    def update(self, event: str, data: Optional[Any] = None) -> None:
        ...


class Subject:
    """
    Sujeto observable. Los servicios pueden heredar de aquí
    para notificar cambios a la UI u otros observadores.
    """
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event: str, data: Optional[Any] = None) -> None:
        for observer in list(self._observers):
            observer.update(event, data)
