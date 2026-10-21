"""Entidad del dominio: vehículo."""

from dataclasses import dataclass


@dataclass
class Vehicle:
    vehicle_id: int
    arrival_time: float
