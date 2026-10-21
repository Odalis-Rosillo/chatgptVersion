"""Punto de entrada de la simulación."""

from config import (
    ARRIVAL_RATE, GREEN_TIME, MAX_EVENTS, NUM_REPLICAS, RANDOM_SEED,
    RED_TIME, SERVICE_RATE, SIMULATION_TIME,
)
from engine.simulator import TrafficQueueSimulator
from views.console import print_event_sample, print_replica_report, print_summary


def main():
    print("SIMULACIÓN DES DE COLA VEHICULAR CON SEMÁFORO")
    print("=" * 60)
    print(f"Verde: {GREEN_TIME:g} s | Rojo: {RED_TIME:g} s "
          f"| Ciclo: {GREEN_TIME + RED_TIME:g} s")
    print(f"Llegadas: {ARRIVAL_RATE:g} veh/s "
          f"({ARRIVAL_RATE * 3600:.0f} veh/h)")
    print(f"Servicio durante verde: {SERVICE_RATE:g} veh/s "
          f"({SERVICE_RATE * 3600:.0f} veh/h)")
    print(f"Horizonte: {SIMULATION_TIME:g} s | Réplicas: {NUM_REPLICAS}")

    results = []
    first_result = None
    for replica in range(NUM_REPLICAS):
        simulator = TrafficQueueSimulator(
            green_time=GREEN_TIME,
            red_time=RED_TIME,
            arrival_rate=ARRIVAL_RATE,
            service_rate=SERVICE_RATE,
            simulation_time=SIMULATION_TIME,
            seed=RANDOM_SEED + replica,
            max_events=MAX_EVENTS,
        )
        result = simulator.run()
        results.append(result)
        if first_result is None:
            first_result = result
        print_replica_report(replica + 1, result)

    print_summary(results)
    if first_result:
        print_event_sample(first_result)


if __name__ == "__main__":
    main()
