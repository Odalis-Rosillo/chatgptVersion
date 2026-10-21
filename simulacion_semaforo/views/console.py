"""Presentación de resultados para terminal."""

from statistics import mean


def print_replica_report(index, result):
    print(f"\nRéplica {index}")
    print("-" * 60)
    print(f"Horizonte:                     {result['horizon']:.1f} s")
    print(f"Vehículos llegados:            {result['arrivals']}")
    print(f"Vehículos que salieron:        {result['departures']}")
    print(f"Longitud media temporal:       {result['average_queue_length']:.3f} veh")
    print(f"Longitud máxima:               {result['max_queue_length']} veh")
    print(
        "Demora media de los que salieron: "
        f"{result['average_delay_departed']:.3f} s/veh "
        f"(n={result['departed_vehicles_for_delay']})"
    )
    print(f"Vehículos en cola al final:     {result['remaining_vehicles']}")


def print_summary(results):
    print("\nRESUMEN DE RÉPLICAS")
    print("=" * 60)
    fields = [
        ("average_queue_length", "Longitud media temporal", "veh"),
        ("max_queue_length", "Longitud máxima", "veh"),
        ("average_delay_departed", "Demora media de vehículos que salieron", "s/veh"),
        ("remaining_vehicles", "Vehículos en cola al final", "veh"),
    ]
    for key, label, unit in fields:
        values = [r[key] for r in results]
        print(f"{label:<42} media={mean(values):.3f} {unit}")


def print_event_sample(result, limit=15):
    print(f"\nMuestra de los primeros {limit} eventos")
    print("-" * 72)
    print(f"{'tiempo(s)':>10}  {'evento':<18} {'fase':<7} {'cola':>6}  vehículo")
    for event in result["events_log"][:limit]:
        vehicle = event["vehicle_id"] if event["vehicle_id"] is not None else "-"
        print(
            f"{event['time']:10.3f}  {event['event']:<18} "
            f"{event['phase']:<7} {event['queue_length']:6d}  {vehicle}"
        )
