from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Dict, Optional
from zoneinfo import ZoneInfo

from src.dto.ordem_service_dto import OrdemServiceDTO

_BRASILIA_TZ = ZoneInfo("America/Sao_Paulo")


class OrdemService:

    DATETIME_FIELDS = (
        "closing_start_time",
        "closing_end_time",
    )

    BOOLEAN_FIELDS = (
        "cr_hot_air_duct_ok",
        "cr_hot_air_duct_regularized",
        "cr_room_temp_vent_ok",
        "cr_accident_risk",
        "cr_electrical_install_ok",
        "cr_grounding_ok",
        "cr_room_lighting_ok",
        "cr_service_outlet_220v",
        "cr_air_point_for_cleaning",
        "cr_water_point_available",
        "cr_distancing_ok",
        "cr_compressor_ok",
    )

    @staticmethod
    def format_datetime(value: Any) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, datetime):
            dt = value
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            dt = dt.astimezone(_BRASILIA_TZ)
            return dt.strftime("%Y-%m-%dT%H:%M")
        if isinstance(value, str):
            try:
                dt = parsedate_to_datetime(value)
                dt = dt.astimezone(_BRASILIA_TZ)
                return dt.strftime("%Y-%m-%dT%H:%M")
            except (TypeError, ValueError):
                return value
        return str(value)

    @classmethod
    def serialize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Normaliza os campos de ORDEM_SERVICE para a resposta da API:
        datas no formato YYYY-MM-DDTHH:MM e campos booleanos como true/false."""
        for field in cls.DATETIME_FIELDS:
            if field in data:
                data[field] = cls.format_datetime(data[field])

        for field in cls.BOOLEAN_FIELDS:
            if field in data and data[field] is not None:
                data[field] = bool(data[field])

        return data

    def __init__(
        self, 
        id=None,
        OS_number=None,
        id_company=None,
        created_at=None,
        updated_at=None,
        id_equipament=None,
        current_hour_meter=None,
        cga_reason_visit=None,
        cga_reported_defect=None,
        cga_solution_applied=None,
        cga_replaced_parts=None,
        cga_parts_to_replace=None,
        mp_oil=None,
        mp_air_oil_separator_element=None,
        mp_primary_air_filter=None,
        mp_secondary_air_filter=None,
        mp_standard_air_filter=None,
        mp_oil_filter=None,
        mp_engine_lubricant=None,
        mp_coalescing_element=None,
        mp_compressor_element_revision=None,
        rr_lubricating_oil_level=None,
        rr_oil_stock_quantity=None,
        rr_oil_model=None,
        rr_oil_type=None,
        rr_supply_voltage_under_load=None,
        rr_supply_voltage_unloaded=None,
        rr_service_factor_current=None,
        rr_electrical_current_under_load=None,
        rr_electrical_current_unloaded=None,
        rr_fan_motor_current=None,
        rr_compressor_operating_temperature=None,
        rr_dryer_current=None,
        rr_dew_point_temperature=None,
        rr_ambient_temperature=None,
        cr_hot_air_duct_ok=None,
        cr_hot_air_duct_regularized=None,
        cr_room_temp_vent_ok=None,
        cr_room_notes=None,
        cr_install_env_condition=None,
        cr_accident_risk=None,
        cr_electrical_install_ok=None,
        cr_grounding_ok=None,
        cr_room_lighting_ok=None,
        cr_service_outlet_220v=None,
        cr_air_point_for_cleaning=None,
        cr_water_point_available=None,
        cr_distancing_ok=None,
        cr_compressor_ok=None,
        cr_improvement_suggestions=None,
        closing_start_time=None,
        closing_end_time=None,
        closing_responsible=None,
        closing_technician_responsible=None,
        closing_notes=None
    ):
        self.id = id
        self.OS_number = OS_number
        self.id_company = id_company
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()
        self.id_equipament = id_equipament
        self.current_hour_meter = current_hour_meter
        self.cga_reason_visit = cga_reason_visit
        self.cga_reported_defect = cga_reported_defect
        self.cga_solution_applied = cga_solution_applied
        self.cga_replaced_parts = cga_replaced_parts
        self.cga_parts_to_replace = cga_parts_to_replace
        self.mp_oil = mp_oil
        self.mp_air_oil_separator_element = mp_air_oil_separator_element
        self.mp_primary_air_filter = mp_primary_air_filter
        self.mp_secondary_air_filter = mp_secondary_air_filter
        self.mp_standard_air_filter = mp_standard_air_filter
        self.mp_oil_filter = mp_oil_filter
        self.mp_engine_lubricant = mp_engine_lubricant
        self.mp_coalescing_element = mp_coalescing_element
        self.mp_compressor_element_revision = mp_compressor_element_revision
        self.rr_lubricating_oil_level = rr_lubricating_oil_level
        self.rr_oil_stock_quantity = rr_oil_stock_quantity
        self.rr_oil_model = rr_oil_model
        self.rr_oil_type = rr_oil_type
        self.rr_supply_voltage_under_load = rr_supply_voltage_under_load
        self.rr_supply_voltage_unloaded = rr_supply_voltage_unloaded
        self.rr_service_factor_current = rr_service_factor_current
        self.rr_electrical_current_under_load = rr_electrical_current_under_load
        self.rr_electrical_current_unloaded = rr_electrical_current_unloaded
        self.rr_fan_motor_current = rr_fan_motor_current
        self.rr_compressor_operating_temperature = rr_compressor_operating_temperature
        self.rr_dryer_current = rr_dryer_current
        self.rr_dew_point_temperature = rr_dew_point_temperature
        self.rr_ambient_temperature = rr_ambient_temperature
        self.cr_hot_air_duct_ok = cr_hot_air_duct_ok
        self.cr_hot_air_duct_regularized = cr_hot_air_duct_regularized
        self.cr_room_temp_vent_ok = cr_room_temp_vent_ok
        self.cr_room_notes = cr_room_notes
        self.cr_install_env_condition = cr_install_env_condition
        self.cr_accident_risk = cr_accident_risk
        self.cr_electrical_install_ok = cr_electrical_install_ok
        self.cr_grounding_ok = cr_grounding_ok
        self.cr_room_lighting_ok = cr_room_lighting_ok
        self.cr_service_outlet_220v = cr_service_outlet_220v
        self.cr_air_point_for_cleaning = cr_air_point_for_cleaning
        self.cr_water_point_available = cr_water_point_available
        self.cr_distancing_ok = cr_distancing_ok
        self.cr_compressor_ok = cr_compressor_ok
        self.cr_improvement_suggestions = cr_improvement_suggestions
        self.closing_start_time = closing_start_time
        self.closing_end_time = closing_end_time
        self.closing_responsible = closing_responsible
        self.closing_technician_responsible = closing_technician_responsible
        self.closing_notes = closing_notes

    def dto_to_model(self, dto: OrdemServiceDTO):
        for key, value in dto.model_dump(exclude_unset=True).items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        return self

    def to_dict(self):
        return {
            "id": self.id,
            "id_company": self.id_company,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "id_equipament": self.id_equipament,
            "current_hour_meter": self.current_hour_meter,
        }
        