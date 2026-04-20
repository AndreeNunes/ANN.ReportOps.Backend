

from src.model.company import Company


class CompanyRepository:
    def get_all(self, conn, client_id: str):
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM COMPANY WHERE client_id = %s", (client_id,))

        companies_data = cursor.fetchall()

        return companies_data

    def get_by_id(self, id, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM COMPANY WHERE id = %s", (id,))
        company = cursor.fetchone()

        return company

    def create(self, company, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO COMPANY (id, name, document, street, number, complement, neighborhood, city, state, zip_code, phone, email, client_id, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())", (
            company.id, company.name, company.document, company.street, company.number, company.complement, company.neighborhood, company.city, company.state, company.zip_code, company.phone, company.email, company.id_client))
        conn.commit()

    def update(self, company, conn):
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE COMPANY SET name = %s, document = %s, street = %s, number = %s, "
            "complement = %s, neighborhood = %s, city = %s, state = %s, zip_code = %s, "
            "phone = %s, email = %s, updated_at = NOW() WHERE id = %s",
            (company.name, company.document, company.street, company.number,
             company.complement, company.neighborhood, company.city, company.state,
             company.zip_code, company.phone, company.email, company.id)
        )
        conn.commit()

    def delete(self, id, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM COMPANY WHERE id = %s", (id,))
        conn.commit()

    def get_to_equipament(self, conn, client_id: str):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name FROM COMPANY WHERE client_id = %s",
            (client_id,)
        )

        companies_data = cursor.fetchall()

        return companies_data

    def get_company_order_counts(self, conn, client_id: str):
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                os.id_company AS id_company,
                c.name AS label,
                COUNT(os.id) AS total_ordens_service
            FROM COMPANY c
            INNER JOIN ORDEM_SERVICE os ON c.id = os.id_company
            WHERE c.client_id = %s
            GROUP BY os.id_company, c.name
            ORDER BY total_ordens_service DESC
        """

        cursor.execute(query, (client_id,))

        rows = cursor.fetchall()

        return rows

