"""Servicios disponibles en el sistema Software FJ."""

from abc import ABC, abstractmethod
from math import isfinite

from .excepciones import (
    CalculoInconsistenteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)


class Servicio(ABC):
    """Contrato común para los servicios ofrecidos por Software FJ."""

    def __init__(
        self,
        nombre: str,
        tarifa_por_hora: float,
        disponible: bool = True,
    ) -> None:
        self._nombre = self._validar_texto(nombre, "nombre")
        self._tarifa_por_hora = self._validar_numero(
            tarifa_por_hora,
            "tarifa_por_hora",
            minimo=0,
            minimo_exclusivo=True,
        )
        self._disponible = True
        self.disponible = disponible
        self._validar_datos_comunes()

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_por_hora(self) -> float:
        return self._tarifa_por_hora

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        if not isinstance(estado, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser un valor booleano.",
                detalle=estado,
            )
        self._disponible = estado

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ServicioInvalidoError(
                f"El campo {campo} debe ser un texto no vacío.",
                detalle=valor,
            )
        return valor.strip()

    @staticmethod
    def _validar_numero(
        valor: float,
        campo: str,
        minimo: float,
        maximo: float | None = None,
        minimo_exclusivo: bool = False,
    ) -> float:
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ServicioInvalidoError(
                f"El campo {campo} debe ser numérico.",
                detalle=valor,
            )

        try:
            numero = float(valor)
        except OverflowError as error:
            raise ServicioInvalidoError(
                f"El campo {campo} está fuera del rango permitido.",
                detalle=valor,
            ) from error

        if not isfinite(numero):
            raise ServicioInvalidoError(
                f"El campo {campo} debe ser un número finito.",
                detalle=valor,
            )

        fuera_del_minimo = (
            numero <= minimo if minimo_exclusivo else numero < minimo
        )
        if fuera_del_minimo or (maximo is not None and numero > maximo):
            limite = (
                f"mayor que {minimo}"
                if minimo_exclusivo
                else f"entre {minimo} y {maximo}"
            )
            raise ServicioInvalidoError(
                f"El campo {campo} debe ser {limite}.",
                detalle=valor,
            )
        return numero

    def _validar_datos_comunes(self) -> None:
        self._validar_texto(self._nombre, "nombre")
        self._validar_numero(
            self._tarifa_por_hora,
            "tarifa_por_hora",
            minimo=0,
            minimo_exclusivo=True,
        )
        if not isinstance(self._disponible, bool):
            raise ServicioInvalidoError(
                "La disponibilidad debe ser un valor booleano.",
                detalle=self._disponible,
            )

    def _calcular_costo_horario(
        self,
        duracion_horas: float,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        if not self.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio '{self.nombre}' no está disponible."
            )

        duracion = self._validar_numero(
            duracion_horas,
            "duracion_horas",
            minimo=0,
            minimo_exclusivo=True,
        )
        tasa_impuesto = self._validar_numero(
            impuesto,
            "impuesto",
            minimo=0,
            maximo=1,
        )
        tasa_descuento = self._validar_numero(
            descuento,
            "descuento",
            minimo=0,
            maximo=1,
        )

        total = (
            self.tarifa_por_hora
            * duracion
            * (1 - tasa_descuento)
            * (1 + tasa_impuesto)
        )
        if not isfinite(total) or total < 0:
            raise CalculoInconsistenteError(
                "El costo calculado no es un valor finito y no negativo.",
                detalle=total,
            )
        return round(total, 2)

    @abstractmethod
    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        """Calcula el costo para una duración, aplicando tasas opcionales."""

    @abstractmethod
    def describir_servicio(self) -> str:
        """Devuelve una descripción legible del servicio."""

    @abstractmethod
    def validar_parametros(self) -> None:
        """Valida los datos comunes y específicos del servicio."""


class ServicioReservaSala(Servicio):
    """Servicio de reserva de una sala con capacidad definida."""

    def __init__(
        self,
        nombre: str,
        tarifa_por_hora: float,
        capacidad_personas: int,
        disponible: bool = True,
    ) -> None:
        super().__init__(nombre, tarifa_por_hora, disponible)
        self._capacidad_personas = capacidad_personas
        self.validar_parametros()

    @property
    def capacidad_personas(self) -> int:
        return self._capacidad_personas

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        return self._calcular_costo_horario(
            duracion_horas,
            impuesto,
            descuento,
        )

    def describir_servicio(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Sala '{self.nombre}' para {self.capacidad_personas} personas; "
            f"tarifa: {self.tarifa_por_hora:.2f} por hora; {estado}."
        )

    def validar_parametros(self) -> None:
        self._validar_datos_comunes()
        if (
            isinstance(self._capacidad_personas, bool)
            or not isinstance(self._capacidad_personas, int)
            or self._capacidad_personas <= 0
        ):
            raise ServicioInvalidoError(
                "La capacidad de la sala debe ser un entero positivo.",
                detalle=self._capacidad_personas,
            )


class ServicioAlquilerEquipo(Servicio):
    """Servicio de alquiler de un equipo identificado por categoría."""

    def __init__(
        self,
        nombre: str,
        tarifa_por_hora: float,
        tipo_equipo: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(nombre, tarifa_por_hora, disponible)
        self._tipo_equipo = tipo_equipo
        self.validar_parametros()

    @property
    def tipo_equipo(self) -> str:
        return self._tipo_equipo

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        return self._calcular_costo_horario(
            duracion_horas,
            impuesto,
            descuento,
        )

    def describir_servicio(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Alquiler de {self.tipo_equipo} '{self.nombre}'; "
            f"tarifa: {self.tarifa_por_hora:.2f} por hora; {estado}."
        )

    def validar_parametros(self) -> None:
        self._validar_datos_comunes()
        self._tipo_equipo = self._validar_texto(
            self._tipo_equipo,
            "tipo_equipo",
        )


class ServicioAsesoriaEspecializada(Servicio):
    """Servicio de asesoría con una especialidad definida."""

    def __init__(
        self,
        nombre: str,
        tarifa_por_hora: float,
        especialidad: str,
        disponible: bool = True,
    ) -> None:
        super().__init__(nombre, tarifa_por_hora, disponible)
        self._especialidad = especialidad
        self.validar_parametros()

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def calcular_costo(
        self,
        duracion_horas: float,
        impuesto: float = 0.0,
        descuento: float = 0.0,
    ) -> float:
        return self._calcular_costo_horario(
            duracion_horas,
            impuesto,
            descuento,
        )

    def describir_servicio(self) -> str:
        estado = "disponible" if self.disponible else "no disponible"
        return (
            f"Asesoría en {self.especialidad} ('{self.nombre}'); "
            f"tarifa: {self.tarifa_por_hora:.2f} por hora; {estado}."
        )

    def validar_parametros(self) -> None:
        self._validar_datos_comunes()
        self._especialidad = self._validar_texto(
            self._especialidad,
            "especialidad",
        )
