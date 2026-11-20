"""Prueba secuencial de EntidadBase y Clientes para el sistema Software FJ."""

from .cliente import Clientes
from .excepciones import ClienteInvalidoError
from .registro_logs import ARCHIVO_LOG, configurar_logs, registrar_evento


def ejecutar_pruebas_secuenciales() -> None:
    """Ejecuta casos válidos e inválidos paso a paso y verifica el log."""
    configurar_logs()
    registrar_evento("Inicio de prueba secuencial de EntidadBase y Clientes.")

    print("--- Paso 1: Crear un cliente válido ---")
    try:
        cliente_1 = Cliente(
            id_cliente=101,
            nombre="  Laura Martínez  ",
            correo="LAURA.MARTINEZ@CORREO.COM",
            telefono="+57 300 456 7890",
            documento="1098765432",
        )
    except ClienteInvalidoError as exc:
        print(f"Error inesperado al crear cliente válido: {exc}")
        return
    else:
        print("Creado:", cliente_1)
        print("Documento:", cliente_1.documento)
    finally:
        print("Paso 1 finalizado.\n")

    print("--- Paso 2: Activar, desactivar y actualizar contacto válido ---")
    cliente_1.desactivar()
    print("Tras desactivar:", cliente_1.resumen())
    cliente_1.activar()
    print("Tras activar:", cliente_1.resumen())

    try:
        cliente_1.actualizar_contacto(
            correo="laura.nueva@correo.com",
            telefono="3159876543",
        )
    except ClienteInvalidoError as exc:
        print(f"Error inesperado al actualizar contacto: {exc}")
    else:
        print("Contacto actualizado:", cliente_1.resumen())
    finally:
        print("Paso 2 finalizado.\n")

    print("--- Paso 3: Actualización atómica fallida (correo inválido) ---")
    correo_antes = cliente_1.correo
    try:
        cliente_1.actualizar_contacto(correo="correo-sin-arroba")
    except ClienteInvalidoError as exc:
        print("Excepción controlada correctamente:", exc)
        print("Correo conservado tras fallo:", cliente_1.correo == correo_antes)
    finally:
        print("Paso 3 finalizado y programa estable.\n")

    print("--- Paso 4: ID inválido con encadenamiento de excepciones ---")
    try:
        Cliente(
            id_cliente=-1,
            nombre="Carlos Ruiz",
            correo="carlos@correo.com",
            telefono="3101112233",
        )
    except ClienteInvalidoError as exc:
        print("ClienteInvalidoError capturado:", exc)
        print("Causa encadenada (__cause__):", type(exc.__cause__).__name__, "-", exc.__cause__)
    finally:
        print("Paso 4 finalizado y programa estable.\n")

    print("--- Paso 5: Verificar contenido reciente del archivo de logs ---")
    if ARCHIVO_LOG.exists():
        lineas = ARCHIVO_LOG.read_text(encoding="utf-8").splitlines()
        print(f"Archivo de log: {ARCHIVO_LOG}")
        for linea in lineas[-8:]:
            print("  ", linea)
    else:
        print("Aún no se ha generado el archivo de log.")


if __name__ == "__main__":
    ejecutar_pruebas_secuenciales()
