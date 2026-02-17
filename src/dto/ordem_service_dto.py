from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrdemServiceDTO(BaseModel):
    id: Optional[str] = None
    OS_number: Optional[str] = None
    
    id_company: str

    id_equipament: Optional[str] = None

    cga_reason_visit: Optional[str] = None
    cga_reported_defect: Optional[str] = None
    cga_solution_applied: Optional[str] = None
    cga_replaced_parts: Optional[str] = None
    cga_parts_to_replace: Optional[str] = None

    mp_oil: Optional[str] = None
    mp_air_oil_separator_element: Optional[str] = None
    mp_primary_air_filter: Optional[str] = None
    mp_secondary_air_filter: Optional[str] = None
    mp_standard_air_filter: Optional[str] = None
    mp_oil_filter: Optional[str] = None
    mp_engine_lubricant: Optional[str] = None
    mp_coalescing_element: Optional[str] = None
    mp_compressor_element_revision: Optional[str] = None

    rr_lubricating_oil_level: Optional[str] = None
    rr_oil_stock_quantity: Optional[str] = None
    rr_oil_model: Optional[str] = None
    rr_oil_type: Optional[str] = None
    rr_supply_voltage_under_load: Optional[str] = None
    rr_supply_voltage_unloaded: Optional[str] = None
    rr_service_factor_current: Optional[str] = None
    rr_electrical_current_under_load: Optional[str] = None
    rr_electrical_current_unloaded: Optional[str] = None
    rr_fan_motor_current: Optional[str] = None
    rr_compressor_operating_temperature: Optional[str] = None
    rr_dryer_current: Optional[str] = None
    rr_dew_point_temperature: Optional[str] = None
    rr_ambient_temperature: Optional[str] = None

    cr_hot_air_duct_ok: Optional[bool] = None
    cr_hot_air_duct_regularized: Optional[bool] = None
    cr_room_temp_vent_ok: Optional[bool] = None
    cr_room_notes: Optional[str] = None
    cr_install_env_condition: Optional[str] = None
    cr_accident_risk: Optional[bool] = None
    cr_electrical_install_ok: Optional[bool] = None
    cr_grounding_ok: Optional[bool] = None
    cr_room_lighting_ok: Optional[bool] = None
    cr_service_outlet_220v: Optional[bool] = None
    cr_air_point_for_cleaning: Optional[bool] = None
    cr_water_point_available: Optional[bool] = None
    cr_distancing_ok: Optional[bool] = None
    cr_compressor_ok: Optional[bool] = None
    cr_improvement_suggestions: Optional[str] = None

    closing_start_time: Optional[datetime] = None
    closing_end_time: Optional[datetime] = None
    closing_responsible: Optional[str] = None
    closing_technician_responsible: Optional[str] = None
    closing_notes: Optional[str] = None
