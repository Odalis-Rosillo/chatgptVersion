"""Semáforo de ciclo fijo con fases verde y rojo."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrafficLight:
    green_time: float
    red_time: float

    def __post_init__(self):
        if self.green_time <= 0 or self.red_time <= 0:
            raise ValueError("Los tiempos verde y rojo deben ser positivos.")

    @property
    def cycle_time(self) -> float:
        return self.green_time + self.red_time

    def phase_at(self, time: float) -> str:
        position = time % self.cycle_time
        return "GREEN" if position < self.green_time else "RED"

    def next_phase_change(self, time: float) -> float:
        """Devuelve el siguiente instante de cambio de fase."""
        position = time % self.cycle_time
        if position < self.green_time:
            return time + (self.green_time - position)
        return time + (self.cycle_time - position)
