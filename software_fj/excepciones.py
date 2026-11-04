# excepciones.py
# excepciones personalizadas para el proyecto Software FJ.

class SoftwareFJError(Exception):
    """Excepcion base: de esta se heredan todas las demas del sistema."""

    def __init__(self, mensaje, detalle=None):
        # Pasamos el mensaje a la clase madre (Exception)
        super().__init__(mensaje)
        # Almacenamo el mensaje y un 'detalle opcional, como el valor que fallo
        self.mensaje = mensaje
        self.detalle = detalle

    def __str__(self):
        # Mensaje que sale al imprimir el error o al guardarlo en el log
        if self.detalle is not None:
            return f"{self.mensaje} (detalle: {self.detalle})"
        return self.mensaje


class ValidacionError(SoftwareFJError):
    """Datos inválidos."""


class ClienteInvalidoError(ValidacionError):
    """Los datos del cliente no cumplen las reglas (nombre, correo, teléfono)."""


class ServicioInvalidoError(ValidacionError):
    """Los parámetros del servicio no son válidos."""


class ReservaInvalidaError(ValidacionError):
    """Los datos de la reserva no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio solicitado no está disponible."""


class OperacionNoPermitidaError(SoftwareFJError):
    """La operación pedida no se puede realizar en el estado actual del objeto."""


class CalculoInconsistenteError(SoftwareFJError):
    """Un cálculo dio un resultado que contradice las reglas del sistema."""


