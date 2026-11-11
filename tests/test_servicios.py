import unittest

from software_fj.excepciones import (
    CalculoInconsistenteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
)
from software_fj.servicios import (
    Servicio,
    ServicioAlquilerEquipo,
    ServicioAsesoriaEspecializada,
    ServicioReservaSala,
)


class ServicioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.servicios = [
            ServicioReservaSala("Sala Norte", 100, 20),
            ServicioAlquilerEquipo("Proyector", 50, "audiovisual"),
            ServicioAsesoriaEspecializada("Asesoría Python", 200, "desarrollo"),
        ]

    def test_servicios_comparten_interfaz_y_calculan_con_tasas_opcionales(
        self,
    ) -> None:
        self.assertTrue(all(isinstance(servicio, Servicio) for servicio in self.servicios))
        for servicio in self.servicios:
            with self.subTest(servicio=servicio.nombre):
                self.assertEqual(
                    servicio.calcular_costo(2, impuesto=0.19, descuento=0.05),
                    round(servicio.tarifa_por_hora * 2 * 0.95 * 1.19, 2),
                )
                self.assertTrue(servicio.describir_servicio())

    def test_rechaza_parametros_especificos_invalidos(self) -> None:
        with self.assertRaises(ServicioInvalidoError):
            ServicioReservaSala("Sala Norte", 100, 0)
        with self.assertRaises(ServicioInvalidoError):
            ServicioAlquilerEquipo("Proyector", 50, " ")
        with self.assertRaises(ServicioInvalidoError):
            ServicioAsesoriaEspecializada("Asesoría", 200, "")

    def test_rechaza_duracion_y_tasas_fuera_de_rango(self) -> None:
        servicio = self.servicios[0]
        for argumentos in (
            (0,),
            (1, 1.01, 0),
            (1, 0, -0.01),
        ):
            with self.subTest(argumentos=argumentos):
                with self.assertRaises(ServicioInvalidoError):
                    servicio.calcular_costo(*argumentos)

    def test_servicio_no_disponible_no_calcula_costo(self) -> None:
        servicio = ServicioAlquilerEquipo(
            "Proyector",
            50,
            "audiovisual",
            disponible=False,
        )
        with self.assertRaises(ServicioNoDisponibleError):
            servicio.calcular_costo(1)

    def test_detecta_costos_fuera_del_rango_finito(self) -> None:
        servicio = ServicioReservaSala("Sala Norte", 1e308, 20)
        with self.assertRaises(CalculoInconsistenteError):
            servicio.calcular_costo(1e308)

    def test_servicio_base_es_abstracto(self) -> None:
        with self.assertRaises(TypeError):
            Servicio("Servicio base", 100)


if __name__ == "__main__":
    unittest.main()
