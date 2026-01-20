from typing import Optional, Dict, Any
from src.model.client import Client


class ClientRepository:
    def create(self, client: Client, conn) -> Client:
        cursor = conn.cursor()
        sql = """
            INSERT INTO CLIENT (
                id, document, street, number, complement, neighborhood, city, state,
                zip_code, phone, email, plan, plan_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            client.id, client.document, client.street, client.number, client.complement,
            client.neighborhood, client.city, client.state, client.zip_code, client.phone,
            client.email, client.plan, client.plan_id
        ))
        cursor.close()
        return client

    def get_by_id(self, client_id: str, conn) -> Optional[Dict[str, Any]]:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CLIENT WHERE id = %s", (client_id,))
        client = cursor.fetchone()
        cursor.close()
        return client

    def get_by_plan_id(self, plan_id: str, conn) -> Optional[Dict[str, Any]]:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM CLIENT WHERE plan_id = %s", (plan_id,))
        client = cursor.fetchone()
        cursor.close()
        return client

