"""Acumulación de métricas a partir de la trayectoria de la cola."""


class Statistics:
    def __init__(self):
        self.queue_area = 0.0
        self.last_time = 0.0
        self.last_queue_length = 0
        self.max_queue_length = 0
        self.departure_delays = []
        self.arrivals = 0
        self.departures = 0
        self.departures_by_cycle = {}
        self.events_log = []

    def update_queue_area(self, now: float) -> None:
        if now < self.last_time:
            raise ValueError("El reloj de simulación no puede retroceder.")
        self.queue_area += self.last_queue_length * (now - self.last_time)
        self.last_time = now

    def queue_changed(self, now: float, queue_length: int) -> None:
        self.update_queue_area(now)
        self.last_queue_length = queue_length
        self.max_queue_length = max(self.max_queue_length, queue_length)

    def log(self, time: float, event: str, phase: str, queue_length: int,
            vehicle_id=None, note="") -> None:
        self.events_log.append({
            "time": round(time, 6),
            "event": event,
            "phase": phase,
            "queue_length": queue_length,
            "vehicle_id": vehicle_id,
            "note": note,
        })

    def report(self, horizon: float, remaining: int) -> dict:
        self.update_queue_area(horizon)
        return {
            "horizon": horizon,
            "arrivals": self.arrivals,
            "departures": self.departures,
            "average_queue_length": self.queue_area / horizon if horizon else 0.0,
            "max_queue_length": self.max_queue_length,
            "average_delay_departed": (
                sum(self.departure_delays) / len(self.departure_delays)
                if self.departure_delays else 0.0
            ),
            "departed_vehicles_for_delay": len(self.departure_delays),
            "remaining_vehicles": remaining,
            "departures_by_cycle": dict(self.departures_by_cycle),
        }
