from src.model.equipament import Equipament


class EquipamentRepository:
    def get_all(self, conn, company_id: str):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM EQUIPAMENT WHERE company_id = %s", (company_id,))
        equipament = cursor.fetchall()
        cursor.close()

        return equipament

    def add(self, equipament: Equipament, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO EQUIPAMENT (id, name, manufacture_date, compressor_unit_model, hmi_model, supply_voltage, intake_solenoid_voltage, serial_number, inverter_softstarter_brand_model, working_pressure, control_voltage, company_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (equipament.id, equipament.name, equipament.manufacture_date, equipament.compressor_unit_model, equipament.hmi_model, equipament.supply_voltage, equipament.intake_solenoid_voltage, equipament.serial_number, equipament.inverter_softstarter_brand_model, equipament.working_pressure, equipament.control_voltage, equipament.company_id, equipament.created_at, equipament.updated_at))
        conn.commit()
        cursor.close()

        return equipament