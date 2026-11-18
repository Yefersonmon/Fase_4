
"""Programa principal del sistema Software FJ."""

from software_fj.servicios import ServicioReservaSala
from software_fj.reservas import Reserva
from software_fj.excepciones import SoftwareFJError
from software_fj.registro_logs import (
    configurar_logs,
    registrar_evento,
    registrar_error,
)


def main():
    """Ejecuta la simulación del sistema de reservas."""

    configurar_logs()

    print("=" * 38)
    print("       SISTEMA SOFTWARE FJ")
    print("  Gestion de clientes y reservas")
    print("=" * 38)

    try:
        # Cliente temporal para realizar la prueba.
        cliente = "Cliente de prueba"

        # Crear un servicio disponible.
        servicio = ServicioReservaSala(
            "Sala de reuniones",
            50000,
            10,
            True
        )

        # Crear una reserva de dos horas.
        reserva = Reserva(cliente, servicio, 2)

        print("\n--- INFORMACION DE LA RESERVA ---")
        reserva.mostrar_reserva()

        # Calcular el costo.
        costo = reserva.calcular_costo()
        print("\nCosto total de la reserva:", costo)

        # Confirmar la reserva.
        print("\n--- CONFIRMACION ---")
        print("Estado antes:", reserva.estado)
        reserva.confirmar_reserva()
        print("Estado despues:", reserva.estado)

        # Procesar la reserva.
        print("\n--- PROCESAMIENTO ---")
        reserva.procesar_reserva()

        # Mostrar el estado final.
        print("\n--- ESTADO FINAL ---")
        reserva.mostrar_reserva()

                # Probar la cancelacion de otra reserva.
        print("\n--- PRUEBA DE CANCELACION ---")
        reserva_cancelacion = Reserva(cliente, servicio, 1)
        reserva_cancelacion.cancelar_reserva()
        reserva_cancelacion.mostrar_reserva()

    except SoftwareFJError as error:
        registrar_error(error)
        print("\nError del sistema:", error)

    except Exception as error:
        registrar_error(error)
        print("\nError inesperado:", error)

    else:
        registrar_evento(
            "La simulacion finalizo correctamente."
        )
        print("\nLa simulacion termino correctamente.")

    finally:
        print("\nFin de la ejecucion del sistema Software FJ.")

if __name__ == "__main__":
    main()
