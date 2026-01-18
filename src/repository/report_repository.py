

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

    def get_by_id_and_app_user_id(self, id, app_user_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM REPORT WHERE id = %s AND id_app_user = %s", (id, app_user_id))
        report = cursor.fetchone()
        cursor.close()

        return Report(**report) if report else None

    def get_by_id_reference_and_app_user_id(self, id_reference, app_user_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM REPORT WHERE id_reference = %s AND id_app_user = %s", (id_reference, app_user_id))
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

    def create(self, report, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO REPORT (id, type, status, id_app_user, id_reference, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, NOW(), NOW())", (report.id, report.type, report.status, report.id_app_user, report.id_reference))
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
                    cga_probable_cause,
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
                    eq_current_hour_meter,
                    id_equipament
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
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
                ordem_service.cga_probable_cause,
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
                ordem_service.eq_current_hour_meter,
                ordem_service.id_equipament
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
                cga_probable_cause = %s,
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
                eq_current_hour_meter = %s,
                id_equipament = %s
            WHERE id = %s
        """

        values = (
            ordem_service.OS_number,
            ordem_service.id_company,
            ordem_service.created_at,
            ordem_service.updated_at,
            ordem_service.cga_reason_visit,
            ordem_service.cga_reported_defect,
            ordem_service.cga_probable_cause,
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
            ordem_service.eq_current_hour_meter,
            ordem_service.id_equipament,
            ordem_service.id
        )

        cursor.execute(sql, values)

        conn.commit()

        cursor.close();

        return True