
"""Gestion de reservas del sistema Software FJ."""

from math import isfinite

from .excepciones import (
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)

from .registro_logs import registrar_evento, registrar_error


class Reserva:
    """Representa una reserva de un cliente para un servicio."""

    def __init__(self, cliente, servicio, duracion):

        # Validar el cliente
        if cliente is None:
            raise ReservaInvalidaError(
                "La reserva debe tener un cliente."
            )

        # Validar el servicio
        if servicio is None:
            raise ReservaInvalidaError(
                "La reserva debe tener un servicio."
            )

        # Validar la duracion
        if (
            isinstance(duracion, bool)
            or not isinstance(duracion, (int, float))
            or not isfinite(duracion)
            or duracion <= 0
        ):
            raise ReservaInvalidaError(
                "La duracion debe ser un numero mayor que cero.",
                detalle=duracion,
            )

        # Comprobar que el servicio tenga los datos necesarios
        if not hasattr(servicio, "calcular_costo"):
            raise ReservaInvalidaError(
                "El servicio no permite calcular costos."
            )

        if not hasattr(servicio, "disponible"):
            raise ReservaInvalidaError(
                "El servicio no tiene atributo de disponibilidad."
            )

        if not servicio.disponible:
            raise ServicioNoDisponibleError(
                "El servicio seleccionado no esta disponible."
            )

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

        registrar_evento("Se creo una nueva reserva.")

    def mostrar_reserva(self):
        """Muestra la informacion de la reserva."""

        print("Cliente:", self.cliente)
        print("Servicio:", self.servicio.nombre)
        print("Duracion:", self.duracion)
        print("Estado:", self.estado)

    def confirmar_reserva(self):
        """Confirma una reserva pendiente."""

        if self.estado != "Pendiente":
            raise OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        self.estado = "Confirmada"
        registrar_evento("Reserva confirmada.")
        print("La reserva ha sido confirmada.")

    def cancelar_reserva(self):
        """Cancela una reserva pendiente o confirmada."""

        if self.estado not in ("Pendiente", "Confirmada"):
            raise OperacionNoPermitidaError(
                "No se puede cancelar una reserva procesada o cancelada."
            )

        self.estado = "Cancelada"
        registrar_evento("Reserva cancelada.")
        print("La reserva ha sido cancelada.")

    def procesar_reserva(self):
        """Procesa una reserva previamente confirmada."""

        if self.estado != "Confirmada":
            raise OperacionNoPermitidaError(
                "Solo se pueden procesar reservas confirmadas."
            )

        self.estado = "Procesada"
        registrar_evento("Reserva procesada.")
        print("La reserva ha sido procesada.")

    def calcular_costo(self, impuesto=0.0, descuento=0.0):
        """Calcula el costo de la reserva usando su servicio."""

        try:
            costo = self.servicio.calcular_costo(
                self.duracion,
                impuesto,
                descuento,
            )

            if (
                isinstance(costo, bool)
                or not isinstance(costo, (int, float))
                or not isfinite(costo)
                or costo < 0
            ):
                raise CalculoInconsistenteError(
                    "El costo calculado no es valido.",
                    detalle=costo,
                )

            registrar_evento("Se calculo el costo de una reserva.")
            return round(costo, 2)

        except CalculoInconsistenteError as error:
            registrar_error(error)
            raise

        except Exception as error:
            registrar_error(error)
            raise CalculoInconsistenteError(
                "No fue posible calcular el costo de la reserva."
            ) from error
