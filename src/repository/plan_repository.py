from typing import Optional, Dict, Any
from src.model.plan import Plan


class PlanRepository:
    def create(self, plan: Plan, conn) -> Plan:
        cursor = conn.cursor()
        sql = "INSERT INTO PLAN (id, access_validate, access_date_valid) VALUES (%s, %s, %s)"
        cursor.execute(sql, (plan.id, plan.access_validate, plan.access_date_valid))
        cursor.close()
        return plan

    def get_by_id(self, plan_id: str, conn) -> Optional[Dict[str, Any]]:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PLAN WHERE id = %s", (plan_id,))
        plan = cursor.fetchone()
        cursor.close()
        return plan

    def get_all_valid(self, conn) -> list[Dict[str, Any]]:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM PLAN WHERE access_date_valid >= NOW()")
        plans = cursor.fetchall()
        cursor.close()
        return plans

