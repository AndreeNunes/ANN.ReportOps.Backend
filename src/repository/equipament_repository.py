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
        cursor.execute(
            """
            INSERT INTO EQUIPAMENT (
                id, name, manufacture_date, current_hour_meter, compressor_unit_model, hmi_model,
                supply_voltage, intake_solenoid_voltage, serial_number,
                inverter_softstarter_brand_model, working_pressure,
                coalescing_filter_model, motor_lubrication_data,
                control_voltage, company_id, created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                equipament.id,
                equipament.name,
                equipament.manufacture_date,
                equipament.current_hour_meter,
                equipament.compressor_unit_model,
                equipament.hmi_model,
                equipament.supply_voltage,
                equipament.intake_solenoid_voltage,
                equipament.serial_number,
                equipament.inverter_softstarter_brand_model,
                equipament.working_pressure,
                equipament.coalescing_filter_model,
                equipament.motor_lubrication_data,
                equipament.control_voltage,
                equipament.company_id,
                equipament.created_at,
                equipament.updated_at
            )
        )
        conn.commit()
        cursor.close()

        return equipament

    def get_by_id(self, conn, id: str, company_id: str):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM EQUIPAMENT WHERE id = %s AND company_id = %s",
            (id, company_id)
        )
        equipament = cursor.fetchone()
        cursor.close()

        return equipament

    def update(self, equipament: Equipament, conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE 
                EQUIPAMENT
            SET
                name = %s,
                manufacture_date = %s,
                current_hour_meter = %s,
                compressor_unit_model = %s,
                hmi_model = %s,
                supply_voltage = %s,
                intake_solenoid_voltage = %s,
                serial_number = %s,
                inverter_softstarter_brand_model = %s,
                working_pressure = %s,
                coalescing_filter_model = %s,
                motor_lubrication_data = %s,
                control_voltage = %s,
                updated_at = %s
            WHERE id = %s AND company_id = %s
            """,
            (
                equipament.name,
                equipament.manufacture_date,
                equipament.current_hour_meter,
                equipament.compressor_unit_model,
                equipament.hmi_model,
                equipament.supply_voltage,
                equipament.intake_solenoid_voltage,
                equipament.serial_number,
                equipament.inverter_softstarter_brand_model,
                equipament.working_pressure,
                equipament.coalescing_filter_model,
                equipament.motor_lubrication_data,
                equipament.control_voltage,
                equipament.updated_at,
                equipament.id,
                equipament.company_id
            )
        )
        conn.commit()
        cursor.close()

        return equipament

    def delete(self, conn, id: str, company_id: str):
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM EQUIPAMENT WHERE id = %s AND company_id = %s",
            (id, company_id)
        )
        conn.commit()
        cursor.close()