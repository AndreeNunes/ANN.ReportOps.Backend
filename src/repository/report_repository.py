

from src.model.ordem_service import OrdemService
from src.model.report import Report


class ReportRepository:

    def get_by_id_and_app_user_id(self, id_reference, app_user_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM REPORT WHERE id_reference = %s AND id_app_user = %s", (id_reference, app_user_id))
        report = cursor.fetchone()
        cursor.close()

        return Report(**report) if report else None

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
                    id_company,
                    created_at,
                    updated_at,
                    cga_reason_visit,
                    cga_reported_defect,
                    cga_probable_cause,
                    cga_solution_applied,
                    cga_replaced_parts,
                    cga_parts_to_replace,
                    pm_oil,
                    pm_air_separator_filter,
                    pm_air_filter,
                    pm_oil_filter,
                    pm_air_oil_filter,
                    pm_belt_condition,
                    pm_coupling_condition,
                    pm_motor_bearing_lubrication,
                    pm_compressor_bearing_lubrication,
                    or_oil_level,
                    or_drain_water_separator,
                    or_motor_current_no_load,
                    or_motor_current_full_load,
                    or_motor_voltage,
                    or_motor_temperature,
                    or_compressor_temperature,
                    or_oil_pressure,
                    or_service_hours_counter,
                    or_air_leak_test,
                    or_cooling_fan_condition,
                    or_cooler_condition,
                    or_coupling_condition_monitor,
                    or_bearing_condition_monitor,
                    or_belt_condition_monitor,
                    or_noise_and_vibration_level,
                    or_electrical_connections_condition,
                    or_other_irregularities,
                    sgac_condition,
                    chk_equipment_has_exhaust_duct,
                    chk_environment_condition,
                    chk_environment_classification,
                    chk_compressor_room_ventilation,
                    chk_fire_risk,
                    chk_noise_protection,
                    chk_electrical_panel_protection,
                    chk_grounding,
                    chk_electrical_panel_disjunction,
                    chk_power_supply_voltage,
                    chk_power_supply_220v,
                    chk_space_for_maintenance,
                    chk_space_for_air_filter_change,
                    chk_space_for_motor_bearing_change,
                    chk_coupling_protection,
                    chk_belt_protection,
                    chk_air_compressor_orientation,
                    closing_start_time,
                    closing_end_time,
                    closing_date,
                    closing_responsible
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """

        values = (
                ordem_service.id,
                ordem_service.id_company,
                ordem_service.created_at,
                ordem_service.updated_at,
                ordem_service.cga_reason_visit,
                ordem_service.cga_reported_defect,
                ordem_service.cga_probable_cause,
                ordem_service.cga_solution_applied,
                ordem_service.cga_replaced_parts,
                ordem_service.cga_parts_to_replace,
                ordem_service.pm_oil,
                ordem_service.pm_air_separator_filter,
                ordem_service.pm_air_filter,
                ordem_service.pm_oil_filter,
                ordem_service.pm_air_oil_filter,
                ordem_service.pm_belt_condition,
                ordem_service.pm_coupling_condition,
                ordem_service.pm_motor_bearing_lubrication,
                ordem_service.pm_compressor_bearing_lubrication,
                ordem_service.or_oil_level,
                ordem_service.or_drain_water_separator,
                ordem_service.or_motor_current_no_load,
                ordem_service.or_motor_current_full_load,
                ordem_service.or_motor_voltage,
                ordem_service.or_motor_temperature,
                ordem_service.or_compressor_temperature,
                ordem_service.or_oil_pressure,
                ordem_service.or_service_hours_counter,
                ordem_service.or_air_leak_test,
                ordem_service.or_cooling_fan_condition,
                ordem_service.or_cooler_condition,
                ordem_service.or_coupling_condition_monitor,
                ordem_service.or_bearing_condition_monitor,
                ordem_service.or_belt_condition_monitor,
                ordem_service.or_noise_and_vibration_level,
                ordem_service.or_electrical_connections_condition,
                ordem_service.or_other_irregularities,
                ordem_service.sgac_condition,
                ordem_service.chk_equipment_has_exhaust_duct,
                ordem_service.chk_environment_condition,
                ordem_service.chk_environment_classification,
                ordem_service.chk_compressor_room_ventilation,
                ordem_service.chk_fire_risk,
                ordem_service.chk_noise_protection,
                ordem_service.chk_electrical_panel_protection,
                ordem_service.chk_grounding,
                ordem_service.chk_electrical_panel_disjunction,
                ordem_service.chk_power_supply_voltage,
                ordem_service.chk_power_supply_220v,
                ordem_service.chk_space_for_maintenance,
                ordem_service.chk_space_for_air_filter_change,
                ordem_service.chk_space_for_motor_bearing_change,
                ordem_service.chk_coupling_protection,
                ordem_service.chk_belt_protection,
                ordem_service.chk_air_compressor_orientation,
                ordem_service.closing_start_time,
                ordem_service.closing_end_time,
                ordem_service.closing_date,
                ordem_service.closing_responsible
            )

        cursor.execute(sql, values)

        conn.commit()
        cursor.close();

        return True