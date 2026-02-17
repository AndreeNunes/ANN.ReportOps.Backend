

import json
from src.model.ordem_service import OrdemService
from src.model.report import Report


class ReportRepository:

    def get_all(self, app_user_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM REPORT WHERE id_app_user = %s", (app_user_id,))
        reports = cursor.fetchall()
        cursor.close()

        return reports

    def get_all_ids(self, app_user_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM REPORT WHERE id_app_user = %s", (app_user_id,))
        rows = cursor.fetchall()
        cursor.close()
        return [row["id"] for row in rows]

    def get_all_ids_by_status(self, id_client, status, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM REPORT WHERE id_client = %s AND status = %s", (id_client, status))
        rows = cursor.fetchall()
        cursor.close()
        return [row["id"] for row in rows]

    def get_by_id_client_and_id(self, id, id_client, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM REPORT WHERE id = %s AND id_client = %s", (id, id_client))
        report = cursor.fetchone()
        cursor.close()

        return Report(**report) if report else None

    def get_by_id_reference_and_id_client(self, id_reference, id_client, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM REPORT WHERE id_reference = %s AND id_client = %s", (id_reference, id_client))
        report = cursor.fetchone()
        cursor.close()

        print("REPORT", report)

        return Report(**report) if report else None

    def get_reference_ordem_service(self, id_reference, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM ORDEM_SERVICE WHERE id = %s", (id_reference,))
        ordem_service = cursor.fetchone()
        cursor.close()

        return ordem_service

    def get_ordem_services_by_report_ids(self, report_ids, id_client, conn):
        if not report_ids:
            return []
        
        cursor = conn.cursor(dictionary=True)
        placeholders = ", ".join(["%s"] * len(report_ids))
        
        sql = f"""
            SELECT
                r.id AS report_id,
                os.*,
                c.id AS company_id,
                c.name AS company_name,
                c.document AS company_document,
                c.street AS company_street,
                c.number AS company_number,
                c.complement AS company_complement,
                c.neighborhood AS company_neighborhood,
                c.city AS company_city,
                c.state AS company_state,
                c.zip_code AS company_zip_code,
                c.phone AS company_phone,
                c.email AS company_email,
                e.id AS equipament_id,
                e.name AS equipament_name,
                e.manufacture_date AS equipament_manufacture_date,
                e.current_hour_meter AS equipament_current_hour_meter,
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
            INNER JOIN ORDEM_SERVICE os ON os.id = r.id_reference
            INNER JOIN COMPANY c ON c.id = os.id_company
            LEFT JOIN EQUIPAMENT e ON e.id = os.id_equipament
            WHERE r.id_client = %s
              AND r.id IN ({placeholders})
        """
        
        params = [id_client] + list(report_ids)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_ordem_service_ids_by_report_ids(self, report_ids, conn):
        if not report_ids:
            return []
        
        cursor = conn.cursor(dictionary=True)

        placeholders = ", ".join(["%s"] * len(report_ids))

        sql = f"""
            SELECT id_reference
            FROM REPORT
            WHERE type = %s
              AND id IN ({placeholders})
        """

        params = ["ORDEM_SERVICE"] + list(report_ids)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return [row["id_reference"] for row in rows]

    def bulk_delete_ordem_service_by_ids(self, ordem_service_ids, conn):
        """
        Deleta em lote em ORDEM_SERVICE pelos IDs informados.
        """
        if not ordem_service_ids:
            return 0
        
        cursor = conn.cursor()
        placeholders = ", ".join(["%s"] * len(ordem_service_ids))
        sql = f"DELETE FROM ORDEM_SERVICE WHERE id IN ({placeholders})"
        cursor.execute(sql, list(ordem_service_ids))
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return affected

    def bulk_delete_reports_by_ids(self, report_ids, conn):
        if not report_ids:
            return 0
        
        cursor = conn.cursor()
        placeholders = ", ".join(["%s"] * len(report_ids))
        sql = f"DELETE FROM REPORT WHERE id IN ({placeholders})"
        params = list(report_ids)
        cursor.execute(sql, params)
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return affected

    def create(self, report, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO REPORT (id, type, status, id_client, id_app_user, id_reference, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())", (report.id, report.type, report.status, report.id_client, report.id_app_user, report.id_reference))
        conn.commit()
        cursor.close()

        return report

    def create_reference(self, report_reference, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO REPORT_REFERENCE (id, type_report, id_report, created_at, updated_at) VALUES (%s, %s, %s, NOW(), NOW())", (report_reference.id, report_reference.type_report, report_reference.id_report))
        conn.commit()
        cursor.close();
        return report_reference

    def create_reference_ordem_service(self, ordem_service: OrdemService, conn):
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO ORDEM_SERVICE (
                    id,
                    OS_number,
                    id_company,
                    created_at,
                    updated_at,
                    cga_reason_visit,
                    cga_reported_defect,
                    cga_solution_applied,
                    cga_replaced_parts,
                    cga_parts_to_replace,
                    mp_oil,
                    mp_air_oil_separator_element,
                    mp_primary_air_filter,
                    mp_secondary_air_filter,
                    mp_standard_air_filter,
                    mp_oil_filter,
                    mp_engine_lubricant,
                    mp_coalescing_element,
                    mp_compressor_element_revision,
                    rr_lubricating_oil_level,
                    rr_oil_stock_quantity,
                    rr_oil_model,
                    rr_oil_type,
                    rr_supply_voltage_under_load,
                    rr_supply_voltage_unloaded,
                    rr_service_factor_current,
                    rr_electrical_current_under_load,
                    rr_electrical_current_unloaded,
                    rr_fan_motor_current,
                    rr_compressor_operating_temperature,
                    rr_dryer_current,
                    rr_dew_point_temperature,
                    rr_ambient_temperature,
                    cr_hot_air_duct_ok,
                    cr_hot_air_duct_regularized,
                    cr_room_temp_vent_ok,
                    cr_room_notes,
                    cr_install_env_condition,
                    cr_accident_risk,
                    cr_electrical_install_ok,
                    cr_grounding_ok,
                    cr_room_lighting_ok,
                    cr_service_outlet_220v,
                    cr_air_point_for_cleaning,
                    cr_water_point_available,
                    cr_distancing_ok,
                    cr_compressor_ok,
                    cr_improvement_suggestions,
                    closing_start_time,
                    closing_end_time,
                    closing_responsible,
                    id_equipament,
                    closing_technician_responsible
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

        values = (
                ordem_service.id,
                ordem_service.OS_number,
                ordem_service.id_company,
                ordem_service.created_at,
                ordem_service.updated_at,
                ordem_service.cga_reason_visit,
                ordem_service.cga_reported_defect,
                ordem_service.cga_solution_applied,
                ordem_service.cga_replaced_parts,
                ordem_service.cga_parts_to_replace,
                ordem_service.mp_oil,
                ordem_service.mp_air_oil_separator_element,
                ordem_service.mp_primary_air_filter,
                ordem_service.mp_secondary_air_filter,
                ordem_service.mp_standard_air_filter,
                ordem_service.mp_oil_filter,
                ordem_service.mp_engine_lubricant,
                ordem_service.mp_coalescing_element,
                ordem_service.mp_compressor_element_revision,
                ordem_service.rr_lubricating_oil_level,
                ordem_service.rr_oil_stock_quantity,
                ordem_service.rr_oil_model,
                ordem_service.rr_oil_type,
                ordem_service.rr_supply_voltage_under_load,
                ordem_service.rr_supply_voltage_unloaded,
                ordem_service.rr_service_factor_current,
                ordem_service.rr_electrical_current_under_load,
                ordem_service.rr_electrical_current_unloaded,
                ordem_service.rr_fan_motor_current,
                ordem_service.rr_compressor_operating_temperature,
                ordem_service.rr_dryer_current,
                ordem_service.rr_dew_point_temperature,
                ordem_service.rr_ambient_temperature,
                ordem_service.cr_hot_air_duct_ok,
                ordem_service.cr_hot_air_duct_regularized,
                ordem_service.cr_room_temp_vent_ok,
                ordem_service.cr_room_notes,
                ordem_service.cr_install_env_condition,
                ordem_service.cr_accident_risk,
                ordem_service.cr_electrical_install_ok,
                ordem_service.cr_grounding_ok,
                ordem_service.cr_room_lighting_ok,
                ordem_service.cr_service_outlet_220v,
                ordem_service.cr_air_point_for_cleaning,
                ordem_service.cr_water_point_available,
                ordem_service.cr_distancing_ok,
                ordem_service.cr_compressor_ok,
                ordem_service.cr_improvement_suggestions,
                ordem_service.closing_start_time,
                ordem_service.closing_end_time,
                ordem_service.closing_responsible,
                ordem_service.id_equipament,
                ordem_service.closing_technician_responsible
            )

        cursor.execute(sql, values)

        conn.commit()
        cursor.close();

        return True


    def update_reference_ordem_service(self, ordem_service: OrdemService, conn):
        cursor = conn.cursor()
        
        sql = """
            UPDATE ORDEM_SERVICE SET
                OS_number = %s,
                id_company = %s,
                created_at = %s,
                updated_at = %s,
                cga_reason_visit = %s,
                cga_reported_defect = %s,
                cga_solution_applied = %s,
                cga_replaced_parts = %s,
                cga_parts_to_replace = %s,
                mp_oil = %s,
                mp_air_oil_separator_element = %s,
                mp_primary_air_filter = %s,
                mp_secondary_air_filter = %s,
                mp_standard_air_filter = %s,
                mp_oil_filter = %s,
                mp_engine_lubricant = %s,
                mp_coalescing_element = %s,
                mp_compressor_element_revision = %s,
                rr_lubricating_oil_level = %s,
                rr_oil_stock_quantity = %s,
                rr_oil_model = %s,
                rr_oil_type = %s,
                rr_supply_voltage_under_load = %s,
                rr_supply_voltage_unloaded = %s,
                rr_service_factor_current = %s,
                rr_electrical_current_under_load = %s,
                rr_electrical_current_unloaded = %s,
                rr_fan_motor_current = %s,
                rr_compressor_operating_temperature = %s,
                rr_dryer_current = %s,
                rr_dew_point_temperature = %s,
                rr_ambient_temperature = %s,
                cr_hot_air_duct_ok = %s,
                cr_hot_air_duct_regularized = %s,
                cr_room_temp_vent_ok = %s,
                cr_room_notes = %s,
                cr_install_env_condition = %s,
                cr_accident_risk = %s,
                cr_electrical_install_ok = %s,
                cr_grounding_ok = %s,
                cr_room_lighting_ok = %s,
                cr_service_outlet_220v = %s,
                cr_air_point_for_cleaning = %s,
                cr_water_point_available = %s,
                cr_distancing_ok = %s,
                cr_compressor_ok = %s,
                cr_improvement_suggestions = %s,
                closing_start_time = %s,
                closing_end_time = %s,
                closing_responsible = %s,
                id_equipament = %s,
                closing_technician_responsible = %s
            WHERE id = %s
        """

        values = (
            ordem_service.OS_number,
            ordem_service.id_company,
            ordem_service.created_at,
            ordem_service.updated_at,
            ordem_service.cga_reason_visit,
            ordem_service.cga_reported_defect,
            ordem_service.cga_solution_applied,
            ordem_service.cga_replaced_parts,
            ordem_service.cga_parts_to_replace,
            ordem_service.mp_oil,
            ordem_service.mp_air_oil_separator_element,
            ordem_service.mp_primary_air_filter,
            ordem_service.mp_secondary_air_filter,
            ordem_service.mp_standard_air_filter,
            ordem_service.mp_oil_filter,
            ordem_service.mp_engine_lubricant,
            ordem_service.mp_coalescing_element,
            ordem_service.mp_compressor_element_revision,
            ordem_service.rr_lubricating_oil_level,
            ordem_service.rr_oil_stock_quantity,
            ordem_service.rr_oil_model,
            ordem_service.rr_oil_type,
            ordem_service.rr_supply_voltage_under_load,
            ordem_service.rr_supply_voltage_unloaded,
            ordem_service.rr_service_factor_current,
            ordem_service.rr_electrical_current_under_load,
            ordem_service.rr_electrical_current_unloaded,
            ordem_service.rr_fan_motor_current,
            ordem_service.rr_compressor_operating_temperature,
            ordem_service.rr_dryer_current,
            ordem_service.rr_dew_point_temperature,
            ordem_service.rr_ambient_temperature,
            ordem_service.cr_hot_air_duct_ok,
            ordem_service.cr_hot_air_duct_regularized,
            ordem_service.cr_room_temp_vent_ok,
            ordem_service.cr_room_notes,
            ordem_service.cr_install_env_condition,
            ordem_service.cr_accident_risk,
            ordem_service.cr_electrical_install_ok,
            ordem_service.cr_grounding_ok,
            ordem_service.cr_room_lighting_ok,
            ordem_service.cr_service_outlet_220v,
            ordem_service.cr_air_point_for_cleaning,
            ordem_service.cr_water_point_available,
            ordem_service.cr_distancing_ok,
            ordem_service.cr_compressor_ok,
            ordem_service.cr_improvement_suggestions,
            ordem_service.closing_start_time,
            ordem_service.closing_end_time,
            ordem_service.closing_responsible,
            ordem_service.id_equipament,
            ordem_service.closing_technician_responsible,
            ordem_service.id
        )

        cursor.execute(sql, values)

        conn.commit()

        cursor.close();

        return True