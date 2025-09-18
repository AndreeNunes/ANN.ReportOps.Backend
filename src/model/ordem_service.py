from datetime import datetime
from src.dto.ordem_service_dto import OrdemServiceDTO


class OrdemService:
    def __init__(
        self, 
        id=None, 
        id_company=None,
        created_at=None,
        updated_at=None,
        cga_reason_visit=None,
        cga_reported_defect=None,
        cga_probable_cause=None,
        cga_solution_applied=None,
        cga_replaced_parts=None,
        cga_parts_to_replace=None,
        pm_oil=None,
        pm_air_separator_filter=None,
        pm_air_filter=None,
        pm_oil_filter=None,
        pm_air_oil_filter=None,
        pm_belt_condition=None,
        pm_coupling_condition=None,
        pm_motor_bearing_lubrication=None,
        pm_compressor_bearing_lubrication=None,
        or_oil_level=None,
        or_drain_water_separator=None,
        or_motor_current_no_load=None,
        or_motor_current_full_load=None,
        or_motor_voltage=None,
        or_motor_temperature=None,
        or_compressor_temperature=None,
        or_oil_pressure=None,
        or_service_hours_counter=None,
        or_air_leak_test=None,
        or_cooling_fan_condition=None,
        or_cooler_condition=None,
        or_coupling_condition_monitor=None,
        or_bearing_condition_monitor=None,
        or_belt_condition_monitor=None,
        or_noise_and_vibration_level=None,
        or_electrical_connections_condition=None,
        or_other_irregularities=None,
        sgac_condition=None,
        chk_equipment_has_exhaust_duct=None,
        chk_environment_condition=None,
        chk_environment_classification=None,
        chk_compressor_room_ventilation=None,
        chk_fire_risk=None,
        chk_noise_protection=None,
        chk_electrical_panel_protection=None,
        chk_grounding=None,
        chk_electrical_panel_disjunction=None,
        chk_power_supply_voltage=None,
        chk_power_supply_220v=None,
        chk_space_for_maintenance=None,
        chk_space_for_air_filter_change=None,
        chk_space_for_motor_bearing_change=None,
        chk_coupling_protection=None,
        chk_belt_protection=None,
        chk_air_compressor_orientation=None,
        closing_start_time=None,
        closing_end_time=None,
        closing_date=None,
        closing_responsible=None
    ):
        self.id = id
        self.id_company = id_company
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.cga_reason_visit = cga_reason_visit
        self.cga_reported_defect = cga_reported_defect
        self.cga_probable_cause = cga_probable_cause
        self.cga_solution_applied = cga_solution_applied
        self.cga_replaced_parts = cga_replaced_parts
        self.cga_parts_to_replace = cga_parts_to_replace
        self.pm_oil = pm_oil
        self.pm_air_separator_filter = pm_air_separator_filter
        self.pm_air_filter = pm_air_filter
        self.pm_oil_filter = pm_oil_filter
        self.pm_air_oil_filter = pm_air_oil_filter
        self.pm_belt_condition = pm_belt_condition
        self.pm_coupling_condition = pm_coupling_condition
        self.pm_motor_bearing_lubrication = pm_motor_bearing_lubrication
        self.pm_compressor_bearing_lubrication = pm_compressor_bearing_lubrication
        self.or_oil_level = or_oil_level
        self.or_drain_water_separator = or_drain_water_separator
        self.or_motor_current_no_load = or_motor_current_no_load
        self.or_motor_current_full_load = or_motor_current_full_load
        self.or_motor_voltage = or_motor_voltage
        self.or_motor_temperature = or_motor_temperature
        self.or_compressor_temperature = or_compressor_temperature
        self.or_oil_pressure = or_oil_pressure
        self.or_service_hours_counter = or_service_hours_counter
        self.or_air_leak_test = or_air_leak_test
        self.or_cooling_fan_condition = or_cooling_fan_condition
        self.or_cooler_condition = or_cooler_condition
        self.or_coupling_condition_monitor = or_coupling_condition_monitor
        self.or_bearing_condition_monitor = or_bearing_condition_monitor
        self.or_belt_condition_monitor = or_belt_condition_monitor
        self.or_noise_and_vibration_level = or_noise_and_vibration_level
        self.or_electrical_connections_condition = or_electrical_connections_condition
        self.or_other_irregularities = or_other_irregularities
        self.sgac_condition = sgac_condition
        self.chk_equipment_has_exhaust_duct = chk_equipment_has_exhaust_duct
        self.chk_environment_condition = chk_environment_condition
        self.chk_environment_classification = chk_environment_classification
        self.chk_compressor_room_ventilation = chk_compressor_room_ventilation
        self.chk_fire_risk = chk_fire_risk
        self.chk_noise_protection = chk_noise_protection
        self.chk_electrical_panel_protection = chk_electrical_panel_protection
        self.chk_grounding = chk_grounding
        self.chk_electrical_panel_disjunction = chk_electrical_panel_disjunction
        self.chk_power_supply_voltage = chk_power_supply_voltage
        self.chk_power_supply_220v = chk_power_supply_220v
        self.chk_space_for_maintenance = chk_space_for_maintenance
        self.chk_space_for_air_filter_change = chk_space_for_air_filter_change
        self.chk_space_for_motor_bearing_change = chk_space_for_motor_bearing_change
        self.chk_coupling_protection = chk_coupling_protection
        self.chk_belt_protection = chk_belt_protection
        self.chk_air_compressor_orientation = chk_air_compressor_orientation
        self.closing_start_time = closing_start_time
        self.closing_end_time = closing_end_time
        self.closing_date = closing_date
        self.closing_responsible = closing_responsible

    def dto_to_model(self, dto: OrdemServiceDTO):
        for key, value in dto.model_dump(exclude_unset=True).items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        return self
        