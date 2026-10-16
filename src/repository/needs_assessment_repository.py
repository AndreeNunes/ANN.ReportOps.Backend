from src.dto.needs_assessment_dto import NeedsAssessmentDTO


class NeedsAssessmentRepository:
    COLUMNS = (
        "id_company", "id_equipament", "external_compressor_notes",
        "internal_compressor_notes", "air_filter", "oil_filter",
        "air_oil_separator", "pre_coalescing", "post_coalescing",
        "belts", "hoses",
    )

    def validate_relations(self, dto: NeedsAssessmentDTO, client_id: str, conn) -> bool:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM COMPANY WHERE id = %s AND client_id = %s",
                (dto.id_company, client_id),
            )
            if cursor.fetchone() is None:
                return False
            if dto.id_equipament:
                cursor.execute(
                    "SELECT 1 FROM EQUIPAMENT WHERE id = %s AND company_id = %s",
                    (dto.id_equipament, dto.id_company),
                )
                if cursor.fetchone() is None:
                    return False
            return True
        finally:
            cursor.close()

    def get_by_id(self, reference_id: str, conn, for_update: bool = False):
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM NEEDS_ASSESSMENT WHERE id = %s" + (" FOR UPDATE" if for_update else ""),
                (reference_id,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def upsert(self, reference_id: str, dto: NeedsAssessmentDTO, conn):
        values = dto.dict()
        columns = ", ".join(self.COLUMNS)
        placeholders = ", ".join(["%s"] * len(self.COLUMNS))
        updates = ", ".join(f"{field} = VALUES({field})" for field in self.COLUMNS)
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"INSERT INTO NEEDS_ASSESSMENT (id, {columns}) VALUES (%s, {placeholders}) "
                f"ON DUPLICATE KEY UPDATE {updates}, updated_at = CURRENT_TIMESTAMP(6)",
                (reference_id, *(values[field] for field in self.COLUMNS)),
            )
            conn.commit()
        finally:
            cursor.close()
        return self.get_by_id(reference_id, conn)

    def get_by_report_ids(self, report_ids, client_id, conn):
        if not report_ids:
            return []
        placeholders = ", ".join(["%s"] * len(report_ids))
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                f"""
                SELECT r.id AS report_id, n.*,
                    c.id AS company_id, c.name AS company_name,
                    e.id AS equipament_id, e.name AS equipament_name,
                    e.manufacture_date AS equipament_manufacture_date,
                    e.compressor_unit_model AS equipament_compressor_unit_model,
                    e.ihm_model AS equipament_ihm_model,
                    e.supply_voltage AS equipament_supply_voltage,
                    e.intake_solenoid_voltage AS equipament_intake_solenoid_voltage,
                    e.serial_number AS equipament_serial_number,
                    e.inverter_softstarter_brand_model AS equipament_inverter_softstarter_brand_model,
                    e.working_pressure AS equipament_working_pressure,
                    e.coalescing_filter_model AS equipament_coalescing_filter_model,
                    e.motor_lubrication_data AS equipament_motor_lubrication_data,
                    e.control_voltage AS equipament_control_voltage
                FROM REPORT r
                INNER JOIN NEEDS_ASSESSMENT n ON n.id = r.id_reference
                INNER JOIN COMPANY c ON c.id = n.id_company
                LEFT JOIN EQUIPAMENT e ON e.id = n.id_equipament
                WHERE r.id_client = %s AND r.type = 'NEEDS_ASSESSMENT'
                  AND r.id IN ({placeholders})
                """,
                (client_id, *report_ids),
            )
            return cursor.fetchall()
        finally:
            cursor.close()

    def delete_by_ids(self, reference_ids, conn):
        if not reference_ids:
            return 0
        placeholders = ", ".join(["%s"] * len(reference_ids))
        cursor = conn.cursor()
        try:
            cursor.execute(
                f"DELETE FROM REPORT_MEDIA WHERE report_reference_id IN ({placeholders})",
                tuple(reference_ids),
            )
            cursor.execute(
                f"DELETE FROM NEEDS_ASSESSMENT WHERE id IN ({placeholders})",
                tuple(reference_ids),
            )
            count = cursor.rowcount
            conn.commit()
            return count
        finally:
            cursor.close()
