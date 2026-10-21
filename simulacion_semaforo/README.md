# Simulación DES de cola vehicular con semáforo

Proyecto de consola modular en Python. Implementa una cola FIFO, llegadas Poisson
mediante tiempos entre llegadas exponenciales, servicio periódico únicamente
durante verde, registro de eventos y varias réplicas reproducibles.

## Estructura

- `models/`: vehículo, semáforo, cola y estadísticas.
- `engine/`: motor de eventos discretos.
- `views/`: reportes de consola.
- `config.py`: parámetros.
- `main.py`: entrada.
- `requirements.txt`: no hay dependencias externas.

## Requisitos

Python 3.10 o posterior. No requiere instalación de paquetes externos.

## Ejecución

Desde la carpeta del proyecto:

```bash
python3 main.py
```

Si se entrega como ZIP:

```bash
unzip simulacion_semaforo.zip
cd simulacion_semaforo
python3 main.py
```

## Parámetros

Edita `config.py`: tiempos de verde/rojo, tasa de llegada, tasa de servicio,
horizonte, número de réplicas y semilla base. Las tasas se expresan en veh/s.

## Interpretación y supuestos

- Una sola cola FIFO y un solo acceso.
- Las llegadas siguen un proceso de Poisson homogéneo.
- El tiempo entre servicios es exponencial no: es fijo e igual a `1 / SERVICE_RATE`.
  Los vehículos salen en intervalos regulares mientras el semáforo está verde.
- No se permite iniciar una salida si su instante cae fuera del verde.
- El amarillo y el despeje se omiten en esta versión inicial.
- La longitud media se calcula como promedio temporal de Q(t), mediante el área
  bajo la curva de la cola dividida por el horizonte.
- La demora media reportada es la de vehículos que salieron antes del fin de la
  simulación. Los vehículos aún en cola se cuentan aparte; por ello la demora
  reportada puede subestimar la demora de todos los vehículos llegados.
- `remaining_vehicles` es la cola al final del horizonte. La cola residual al fin
  de cada verde queda registrada en los eventos de cambio a rojo y puede añadirse
  como métrica específica si se requiere comparar ciclos.

## Nota de modelado

La tasa de servicio se interpreta como capacidad fija en vehículos por segundo,
pero el servicio se implementa como intervalo determinista entre salidas. Esto
corresponde a un servidor periódico durante el verde. Si se desea un proceso de
servicio exponencial, debe cambiarse la programación del próximo evento de salida.
