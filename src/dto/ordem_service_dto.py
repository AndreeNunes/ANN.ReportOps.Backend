from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrdemServiceDTO(BaseModel):
    id_company: str

    cga_reason_visit: Optional[str] = None
    cga_reported_defect: Optional[str] = None
    cga_probable_cause: Optional[str] = None
    cga_solution_applied: Optional[str] = None
    cga_replaced_parts: Optional[str] = None
    cga_parts_to_replace: Optional[str] = None

    pm_oil: Optional[str] = None
    pm_air_separator_filter: Optional[str] = None
    pm_air_filter: Optional[str] = None
    pm_oil_filter: Optional[str] = None
    pm_air_oil_filter: Optional[str] = None
    pm_belt_condition: Optional[str] = None
    pm_coupling_condition: Optional[str] = None
    pm_motor_bearing_lubrication: Optional[str] = None
    pm_compressor_bearing_lubrication: Optional[str] = None

    or_oil_level: Optional[str] = None
    or_drain_water_separator: Optional[str] = None
    or_motor_current_no_load: Optional[str] = None
    or_motor_current_full_load: Optional[str] = None
    or_motor_voltage: Optional[str] = None
    or_motor_temperature: Optional[str] = None
    or_compressor_temperature: Optional[str] = None
    or_oil_pressure: Optional[str] = None
    or_service_hours_counter: Optional[str] = None
    or_air_leak_test: Optional[str] = None
    or_cooling_fan_condition: Optional[str] = None
    or_cooler_condition: Optional[str] = None
    or_coupling_condition_monitor: Optional[str] = None
    or_bearing_condition_monitor: Optional[str] = None
    or_belt_condition_monitor: Optional[str] = None
    or_noise_and_vibration_level: Optional[str] = None
    or_electrical_connections_condition: Optional[str] = None
    or_other_irregularities: Optional[str] = None

    sgac_condition: Optional[str] = None

    chk_equipment_has_exhaust_duct: Optional[bool] = None
    chk_environment_condition: Optional[str] = None
    chk_environment_classification: Optional[str] = None
    chk_compressor_room_ventilation: Optional[bool] = None
    chk_fire_risk: Optional[bool] = None
    chk_noise_protection: Optional[bool] = None
    chk_electrical_panel_protection: Optional[bool] = None
    chk_grounding: Optional[bool] = None
    chk_electrical_panel_disjunction: Optional[bool] = None
    chk_power_supply_voltage: Optional[str] = None
    chk_power_supply_220v: Optional[bool] = None
    chk_space_for_maintenance: Optional[bool] = None
    chk_space_for_air_filter_change: Optional[bool] = None
    chk_space_for_motor_bearing_change: Optional[bool] = None
    chk_coupling_protection: Optional[bool] = None
    chk_belt_protection: Optional[bool] = None
    chk_air_compressor_orientation: Optional[str] = None

    closing_start_time: Optional[datetime] = None
    closing_end_time: Optional[datetime] = None
    closing_date: Optional[datetime] = None
    closing_responsible: Optional[str] = None
