"""Motor DES: procesa llegadas, salidas y cambios de fase cronológicamente."""

import heapq
import itertools
import random

from models.statistics import Statistics
from models.traffic_light import TrafficLight
from models.vehicle import Vehicle
from models.vehicle_queue import VehicleQueue


class TrafficQueueSimulator:
    ARRIVAL = "arrival"
    DEPARTURE = "departure"
    PHASE_CHANGE = "phase_change"

    def __init__(self, green_time, red_time, arrival_rate, service_rate,
                 simulation_time, seed=1, max_events=2_000_000):
        if arrival_rate < 0:
            raise ValueError("La tasa de llegada no puede ser negativa.")
        if service_rate <= 0:
            raise ValueError("La tasa de servicio debe ser positiva.")
        if simulation_time <= 0:
            raise ValueError("El horizonte debe ser positivo.")

        self.light = TrafficLight(green_time, red_time)
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.simulation_time = simulation_time
        self.rng = random.Random(seed)
        self.max_events = max_events
        self.queue = VehicleQueue()
        self.stats = Statistics()
        self.events = []
        self.sequence = itertools.count()
        self.next_vehicle_id = 1
        self.departure_scheduled = False

    def _schedule(self, time, event_type, payload=None):
        if time <= self.simulation_time:
            heapq.heappush(
                self.events, (time, next(self.sequence), event_type, payload)
            )

    def _schedule_next_arrival(self, after_time):
        if self.arrival_rate == 0:
            return
        interarrival = self.rng.expovariate(self.arrival_rate)
        self._schedule(after_time + interarrival, self.ARRIVAL)

    def _schedule_departure_if_possible(self, now):
        if (self.light.phase_at(now) == "GREEN"
                and not self.queue.is_empty()
                and not self.departure_scheduled):
            departure_time = now + 1.0 / self.service_rate
            # No se permite una salida en el instante de fin del verde.
            if self.light.phase_at(departure_time) == "GREEN":
                self.departure_scheduled = True
                self._schedule(departure_time, self.DEPARTURE)

    def run(self):
        self._schedule_next_arrival(0.0)
        self._schedule(self.light.next_phase_change(0.0), self.PHASE_CHANGE)

        processed = 0
        while self.events:
            now, _, event_type, payload = heapq.heappop(self.events)
            if now > self.simulation_time:
                break
            processed += 1
            if processed > self.max_events:
                raise RuntimeError(
                    "Se alcanzó MAX_EVENTS; revise el horizonte o las tasas."
                )

            phase = self.light.phase_at(now)

            if event_type == self.ARRIVAL:
                vehicle = Vehicle(self.next_vehicle_id, now)
                self.next_vehicle_id += 1
                self.queue.enqueue(vehicle)
                self.stats.arrivals += 1
                self.stats.queue_changed(now, len(self.queue))
                self.stats.log(now, "ARRIVAL", phase, len(self.queue),
                               vehicle.vehicle_id)
                self._schedule_next_arrival(now)
                self._schedule_departure_if_possible(now)

            elif event_type == self.DEPARTURE:
                self.departure_scheduled = False
                # Validación defensiva: el servicio solo ocurre en verde.
                if phase == "GREEN" and not self.queue.is_empty():
                    vehicle = self.queue.dequeue()
                    self.stats.departures += 1
                    self.stats.departure_delays.append(now - vehicle.arrival_time)
                    cycle = int(now // self.light.cycle_time)
                    self.stats.departures_by_cycle[cycle] = (
                        self.stats.departures_by_cycle.get(cycle, 0) + 1
                    )
                    self.stats.queue_changed(now, len(self.queue))
                    self.stats.log(now, "DEPARTURE", phase, len(self.queue),
                                   vehicle.vehicle_id)
                    self._schedule_departure_if_possible(now)
                else:
                    self.stats.log(now, "DEPARTURE_SKIPPED", phase,
                                   len(self.queue), note="Servicio no válido")

            elif event_type == self.PHASE_CHANGE:
                new_phase = self.light.phase_at(now)
                self.stats.log(now, "PHASE_CHANGE", new_phase, len(self.queue))
                self._schedule(self.light.next_phase_change(now), self.PHASE_CHANGE)
                # Si se inicia verde, se puede programar el primer servicio.
                if new_phase == "GREEN":
                    self._schedule_departure_if_possible(now)
                else:
                    # Cualquier salida pendiente que cruce el cambio de fase
                    # será descartada al ejecutarse; el flag se libera aquí.
                    self.departure_scheduled = False

        result = self.stats.report(self.simulation_time, len(self.queue))
        result["events_log"] = self.stats.events_log
        return result
