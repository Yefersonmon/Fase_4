"""Entidad abstracta base para las entidades del sistema Software FJ."""

from abc import ABC, abstractmethod
from math import isfinite

from .excepciones import ValidacionError
from .registro_logs import registrar_evento


class EntidadBase(ABC):
    """Clase abstracta que define atributos y contratos comunes de una entidad."""

    def __init__(self, id_entidad: int, activa: bool = True) -> None:
        self._id_entidad = self._validar_id(id_entidad)
        self._activa = True
        self.activa = activa

    @property
    def id_entidad(self) -> int:
        """Retorna el identificador único de la entidad."""
        return self._id_entidad

    @property
    def activa(self) -> bool:
        """Indica si la entidad está activa en el sistema."""
        return self._activa

    @activa.setter
    def activa(self, valor: bool) -> None:
        """Valida y actualiza el estado de activación de la entidad."""
        if not isinstance(valor, bool):
            raise ValidacionError(
                "El estado 'activa' debe ser un valor booleano.",
                detalle=valor,
            )
        self._activa = valor

    @staticmethod
    def _validar_id(id_valor: int) -> int:
        """Valida que el ID sea un entero positivo (excluyendo booleanos)."""
        if isinstance(id_valor, bool) or not isinstance(id_valor, int) or id_valor <= 0:
            raise ValidacionError(
                "El ID de la entidad debe ser un número entero mayor que cero.",
                detalle=id_valor,
            )
        return id_valor

    @staticmethod
    def _validar_texto_no_vacio(valor: str, campo: str, min_longitud: int = 1) -> str:
        """Valida cadenas de texto no vacías y con longitud mínima."""
        if not isinstance(valor, str):
            raise ValidacionError(
                f"El campo '{campo}' debe ser una cadena de texto.",
                detalle=valor,
            )
        limpio = valor.strip()
        if len(limpio) < min_longitud:
            raise ValidacionError(
                f"El campo '{campo}' debe tener al menos {min_longitud} carácter(es).",
                detalle=valor,
            )
        return limpio

    @staticmethod
    def _validar_numero_finito(valor: float, campo: str, minimo: float = 0) -> float:
        """Valida valores numéricos finitos sin aceptar booleanos, NaN, Inf o desbordamientos."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValidacionError(
                f"El campo '{campo}' debe ser numérico.",
                detalle=valor,
            )
        try:
            numero = float(valor)
        except OverflowError as exc:
            raise ValidacionError(
                f"El campo '{campo}' excede el rango numérico permitido.",
                detalle=valor,
            ) from exc

        if not isfinite(numero) or numero < minimo:
            raise ValidacionError(
                f"El campo '{campo}' debe ser un número finito mayor o igual a {minimo}.",
                detalle=valor,
            )
        return numero

    def activar(self) -> None:
        """Marca la entidad como activa y registra el evento."""
        self.activa = True
        registrar_evento(f"{type(self).__name__} ID={self.id_entidad} activada.")

    def desactivar(self) -> None:
        """Marca la entidad como inactiva y registra el evento."""
        self.activa = False
        registrar_evento(f"{type(self).__name__} ID={self.id_entidad} desactivada.")

    @abstractmethod
    def resumen(self) -> str:
        """Devuelve un resumen legible de la entidad."""

    @abstractmethod
    def validar(self) -> None:
        """Ejecuta las validaciones específicas de la entidad."""
