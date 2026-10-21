"""Parámetros configurables para la simulación."""

# Tiempos en segundos. El ciclo inicial contiene únicamente rojo y verde.
GREEN_TIME = 30.0
RED_TIME = 30.0
SIMULATION_TIME = 3600.0

# Tasas expresadas en vehículos por segundo.
ARRIVAL_RATE = 0.25       # 900 vehículos/hora
SERVICE_RATE = 0.50       # 1800 vehículos/hora durante el verde

NUM_REPLICAS = 5
RANDOM_SEED = 2026

# Número máximo de eventos procesados por corrida como protección.
MAX_EVENTS = 2_000_000
