from datetime import datetime
import uuid

from src.dto.equipament_dto import EquipamentDTO


class Equipament:
    def __init__(self, id: str = None, 
        name: str = None, 
        manufacture_date: str = None,
        current_hour_meter: str = None,
        compressor_unit_model: str = None, 
        ihm_model: str = None, 
        supply_voltage: str = None, 
        intake_solenoid_voltage: str = None,        
        serial_number: str = None,      
        inverter_softstarter_brand_model: str = None,    
        working_pressure: str = None,        
        coalescing_filter_model: str = None,
        motor_lubrication_data: str = None,
        control_voltage: str = None, company_id: str = None, 
        created_at: datetime = None, 
        updated_at: datetime = None):
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.manufacture_date = manufacture_date
        self.current_hour_meter = current_hour_meter
        self.compressor_unit_model = compressor_unit_model
        self.ihm_model = ihm_model
        self.supply_voltage = supply_voltage
        self.intake_solenoid_voltage = intake_solenoid_voltage
        self.serial_number = serial_number
        self.inverter_softstarter_brand_model = inverter_softstarter_brand_model
        self.working_pressure = working_pressure
        self.coalescing_filter_model = coalescing_filter_model
        self.motor_lubrication_data = motor_lubrication_data
        self.control_voltage = control_voltage
        self.company_id = company_id,
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manufacture_date": self.manufacture_date,
            "current_hour_meter": self.current_hour_meter,
            "compressor_unit_model": self.compressor_unit_model,
            "ihm_model": self.ihm_model,
            "supply_voltage": self.supply_voltage,
            "intake_solenoid_voltage": self.intake_solenoid_voltage,
            "serial_number": self.serial_number,
            "inverter_softstarter_brand_model": self.inverter_softstarter_brand_model,
            "working_pressure": self.working_pressure,
            "coalescing_filter_model": self.coalescing_filter_model,
            "motor_lubrication_data": self.motor_lubrication_data,
            "control_voltage": self.control_voltage,
            "company_id": self.company_id
        }

    def dto_to_model(self, dto: EquipamentDTO):
        for key, value in dto.model_dump(exclude_unset=True).items():
            if hasattr(self, key):
                setattr(self, key, value)
                
        return self