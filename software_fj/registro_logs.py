# Registro_logs.py
# Registro de eventos y errores del sistema FJ en un archivo de logs

import logging
from pathlib import Path

# Carpeta y archivo donde se guardan los logs (siempre dentro del proyecto)
RUTA_LOGS = Path(__file__).resolve().parent.parent / "logs"
ARCHIVO_LOG = RUTA_LOGS / "eventos.log"

# Cajal de logs del sistema: todos los modulos usan este mismo
logger = logging.getLogger("Softwarefj")


def configurar_logs():
    """Preparar el archivo de logs. se llama una sola vez al arrancar el programa."""
   
    # Si ya esta configurado no agregamos otro manejador para evitar lineas repetidas
    if logger .handlers:
        return

    # Nos aseguramos de que exista la carpeta log
    RUTA_LOGS.mkdir(exist_ok=True)

    # Registramos los mensajes de diferentes niveles (INFO, WARNING, ERROR)
    logger.setLevel(logging.INFO)

    # el manejador decide a donde van los mensajes: aqui al archivo de logs
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")

    # Formato de los mensajes: fecha, nivel y mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    manejador.setFormatter(formato)

    logger.addHandler(manejador)


def registrar_evento(mensaje):
    """Escribe un evento normal del sistema (nnivel INFO)."""
    logger.info(mensaje)


def registrar_error(error):
    """Escribe un error en el log, incluendo la causa si estaba encadenado."""
    # Texto Base: nombra la clase del error y su mensaje
    texto = f"{type(error).__name__}: {error}"

    # Si el error viene encadenado (raise ... from ...) agregamos la causa
    causa = error.__cause__
    if causa is not None:
        texto += f" | Causa: {type(causa).__name__}: {causa}"

    logger.error(texto)
