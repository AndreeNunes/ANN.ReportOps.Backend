from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class EquipamentDTO(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    manufacture_date: Optional[str] = None
    current_hour_meter: Optional[str] = None
    compressor_unit_model: Optional[str] = None
    ihm_model: Optional[str] = None
    supply_voltage: Optional[str] = None
    intake_solenoid_voltage: Optional[str] = None
    serial_number: Optional[str] = None
    inverter_softstarter_brand_model: Optional[str] = None
    working_pressure: Optional[str] = None
    coalescing_filter_model: Optional[str] = None
    motor_lubrication_data: Optional[str] = None
    control_voltage: Optional[str] = None