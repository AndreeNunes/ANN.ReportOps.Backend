

from src.model.company import Company


class CompanyRepository:
    def get_all(self, conn, client_id: str):
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM COMPANY WHERE client_id = %s", (client_id,))

        companies_data = cursor.fetchall()

        return companies_data

    def get_by_id(self, id, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM COMPANY WHERE ID = %s", (id,))
        company = cursor.fetchone()

        return company

    def create(self, company, conn):
        cursor = conn.cursor()
        cursor.execute("INSERT INTO COMPANY (ID, NAME, DOCUMENT, STREET, NUMBER, COMPLEMENT, NEIGHBORHOOD, CITY, STATE, ZIP_CODE, PHONE, EMAIL, id_client) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
            company.id, company.name, company.document, company.street, company.number, company.complement, company.neighborhood, company.city, company.state, company.zip_code, company.phone, company.email, company.id_client))
        conn.commit()

    def delete(self, id, conn):
        cursor = conn.cursor()
        cursor.execute("DELETE FROM COMPANY WHERE ID = %s", (id,))
        conn.commit()
