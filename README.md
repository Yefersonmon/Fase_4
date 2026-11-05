# Software FJ

Sistema de gestión de clientes, servicios y reservas (trabajo colabortivo) hecho en Python con programación orientada a objetos. Fase 4 del curso Programación (213023) grupo 644, UNAD.

## Cómo ejecutarlo
Requiere Python 3.11 o superior.
python main.py

## Como se usan las excepciones y los logs 

Se importa lo que se necesita en el modulo:

from software_fj.excepciones import ClienteInvalidoError
from software_fj.registro_logs import configurar_logs, registrar_evento, registrar_error

- 'configurar_logs()' se llama solo una vez, al inicio de 'main.py'.
- 'registrar_evento("texto")' guarda gurda los eventos normales en 'logs/eventos.log'.
- 'registrar_error(error)' guarda los errores. Si la excepción fue encadenada con 'raise ... from ...', también se guarda la causa.

todas las excepciones heredan 'softwareFJError' por eso se pueden capturar juntas con un solo 'except SoftwareFJError'

| Integrante | Parte |
|---|---|
| Yefersonmon | Excepciones y registro de logs |
| pendiente | Entidad base y Cliente |
| pendiente | Servicio y servicios especializados |
| pendiente | Reserva y simulaciones (main.py) |
