

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

    def delete(self, id, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM COMPANY WHERE id = %s", (id,))
        conn.commit()
