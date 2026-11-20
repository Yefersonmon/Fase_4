"""Gestión de clientes en el sistema Software FJ."""

import re

from .entidad_base import EntidadBase
from .excepciones import ClienteInvalidoError, ValidacionError
from .registro_logs import registrar_error, registrar_evento


class Cliente(EntidadBase):
    """Representa un cliente con datos personales encapsulados y validados."""

    _REGEX_CORREO = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _REGEX_TELEFONO = re.compile(r"^\+?[0-9\s\-]{7,15}$")

    def __init__(
        self,
        id_cliente: int,
        nombre: str,
        correo: str,
        telefono: str,
        documento: str | None = None,
        activa: bool = True,
    ) -> None:
        # Encadenamos excepciones si la validación de la entidad base falla
        try:
            super().__init__(id_entidad=id_cliente, activa=activa)
        except ValidacionError as exc:
            error_cliente = ClienteInvalidoError(
                "No se pudo inicializar el cliente por un ID o estado inválido.",
                detalle=id_cliente,
            )
            registrar_error(error_cliente)
            raise error_cliente from exc

        # Atributos privados para encapsulación estricta de datos personales
        self._nombre = ""
        self._correo = ""
        self._telefono = ""
        self._documento = None

        # Asignamos vía propiedades para aplicar validaciones desde el inicio
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        if documento is not None:
            self.documento = documento

        self.validar()
        registrar_evento(f"Cliente registrado correctamente (ID={self.id_entidad}, nombre='{self.nombre}').")

    @property
    def nombre(self) -> str:
        """Retorna el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y actualiza el nombre del cliente."""
        try:
            nombre_limpio = self._validar_texto_no_vacio(valor, "nombre", min_longitud=2)
        except ValidacionError as exc:
            err = ClienteInvalidoError("Nombre de cliente inválido.", detalle=valor)
            registrar_error(err)
            raise err from exc

        self._nombre = nombre_limpio

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida y actualiza el correo electrónico del cliente."""
        if not isinstance(valor, str) or not self._REGEX_CORREO.match(valor.strip()):
            err = ClienteInvalidoError(
                "El correo electrónico del cliente no tiene un formato válido.",
                detalle=valor,
            )
            registrar_error(err)
            raise err

        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Retorna el teléfono de contacto del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida y actualiza el teléfono del cliente."""
        if not isinstance(valor, str) or not self._REGEX_TELEFONO.match(valor.strip()):
            err = ClienteInvalidoError(
                "El teléfono del cliente debe tener entre 7 y 15 dígitos.",
                detalle=valor,
            )
            registrar_error(err)
            raise err

        self._telefono = valor.strip()

    @property
    def documento(self) -> str | None:
        """Retorna el documento de identificación opcional del cliente."""
        return self._documento

    @documento.setter
    def documento(self, valor: str | None) -> None:
        """Valida y actualiza el documento de identificación."""
        if valor is None:
            self._documento = None
            return

        if not isinstance(valor, str) or len(valor.strip()) < 5:
            err = ClienteInvalidoError(
                "El documento de identidad debe ser un texto de al menos 5 caracteres.",
                detalle=valor,
            )
            registrar_error(err)
            raise err

        self._documento = valor.strip()

    def actualizar_contacto(self, correo: str | None = None, telefono: str | None = None) -> None:
        """Actualiza correo y/o teléfono usando try / except / else / finally."""
        operacion_exitosa = False
        try:
            if correo is not None:
                self.correo = correo
            if telefono is not None:
                self.telefono = telefono
            self.validar()
        except ClienteInvalidoError as exc:
            registrar_error(exc)
            raise
        else:
            operacion_exitosa = True
            registrar_evento(f"Datos de contacto actualizados para cliente ID={self.id_entidad}.")
        finally:
            estado_final = "completada" if operacion_exitosa else "fallida"
            registrar_evento(
                f"Intento de actualización de contacto (cliente ID={self.id_entidad}) {estado_final}."
            )

    def validar(self) -> None:
        """Verifica la integridad de todos los campos obligatorios del cliente."""
        self._validar_id(self._id_entidad)
        if not self._nombre or not self._correo or not self._telefono:
            err = ClienteInvalidoError(
                "Faltan datos obligatorios del cliente (nombre, correo o teléfono)."
            )
            registrar_error(err)
            raise err

    def resumen(self) -> str:
        """Devuelve un resumen legible del cliente."""
        estado = "Activo" if self.activa else "Inactivo"
        return f"Cliente #{self.id_entidad} - {self.nombre} ({self.correo}) [{estado}]"

    def __str__(self) -> str:
        """Representación amigable para impresión o integración con Reserva."""
        return self.resumen()
