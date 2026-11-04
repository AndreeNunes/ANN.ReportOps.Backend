class CompanyContactRepository:
    def company_is_owned(self, company_id, client_id, conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM COMPANY WHERE id = %s AND client_id = %s LIMIT 1",
            (company_id, client_id),
        )
        owned = cursor.fetchone() is not None
        cursor.close()
        return owned

    def get_all(self, company_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, company_id, name, email, phone, signature_object_key,
                   signature_content_type, signature_size_bytes, signature_updated_at,
                   created_at, updated_at
            FROM COMPANY_CONTACT
            WHERE company_id = %s AND deleted_at IS NULL
            ORDER BY name, id
            """,
            (company_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_owned(self, company_id, contact_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, company_id, name, email, phone, signature_object_key,
                   signature_content_type, signature_size_bytes, signature_updated_at,
                   created_at, updated_at
            FROM COMPANY_CONTACT
            WHERE id = %s AND company_id = %s AND deleted_at IS NULL
            LIMIT 1
            """,
            (contact_id, company_id),
        )
        row = cursor.fetchone()
        cursor.close()
        return row

    def upsert(self, company_id, contact, conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO COMPANY_CONTACT (id, company_id, name, email, phone, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE
                name = IF(company_id = VALUES(company_id), VALUES(name), name),
                email = IF(company_id = VALUES(company_id), VALUES(email), email),
                phone = IF(company_id = VALUES(company_id), VALUES(phone), phone),
                deleted_at = IF(company_id = VALUES(company_id), NULL, deleted_at),
                updated_at = IF(company_id = VALUES(company_id), NOW(), updated_at)
            """,
            (contact["id"], company_id, contact["name"], contact["email"], contact["phone"]),
        )
        conn.commit()
        cursor.close()

    def deactivate(self, company_id, contact_id, conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE COMPANY_CONTACT
            SET deleted_at = NOW(), updated_at = NOW()
            WHERE id = %s AND company_id = %s AND deleted_at IS NULL
            """,
            (contact_id, company_id),
        )
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return affected

    def update_signature(self, company_id, contact_id, object_key, content_type, size_bytes, conn):
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE COMPANY_CONTACT
            SET signature_object_key = %s,
                signature_content_type = %s,
                signature_size_bytes = %s,
                signature_updated_at = NOW(),
                updated_at = NOW()
            WHERE id = %s AND company_id = %s AND deleted_at IS NULL
            """,
            (object_key, content_type, size_bytes, contact_id, company_id),
        )
        affected = cursor.rowcount
        conn.commit()
        cursor.close()
        return affected
