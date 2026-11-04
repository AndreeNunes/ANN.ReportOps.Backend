class TechnicianRepository:
    def get_all(self, client_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT id, client_id, name, email, phone, signature_object_key, signature_content_type,
            signature_size_bytes, signature_updated_at, created_at, updated_at FROM TENANT_TECHNICIAN
            WHERE client_id=%s AND deleted_at IS NULL ORDER BY name,id""", (client_id,))
        rows = cursor.fetchall(); cursor.close(); return rows
    def get_owned(self, technician_id, client_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""SELECT id, client_id, name, email, phone, signature_object_key, signature_content_type,
            signature_size_bytes, signature_updated_at, created_at, updated_at FROM TENANT_TECHNICIAN
            WHERE id=%s AND client_id=%s AND deleted_at IS NULL LIMIT 1""", (technician_id, client_id))
        row=cursor.fetchone(); cursor.close(); return row
    def upsert(self, item, client_id, conn):
        cursor=conn.cursor(); cursor.execute("""INSERT INTO TENANT_TECHNICIAN (id,client_id,name,email,phone,created_at,updated_at)
          VALUES (%s,%s,%s,%s,%s,NOW(),NOW()) ON DUPLICATE KEY UPDATE
          name=IF(client_id=VALUES(client_id),VALUES(name),name), email=IF(client_id=VALUES(client_id),VALUES(email),email),
          phone=IF(client_id=VALUES(client_id),VALUES(phone),phone), deleted_at=IF(client_id=VALUES(client_id),NULL,deleted_at),
          updated_at=IF(client_id=VALUES(client_id),NOW(),updated_at)""",(item['id'],client_id,item['name'],item['email'],item['phone']))
        conn.commit(); cursor.close()
    def deactivate(self, technician_id, client_id, conn):
        cursor=conn.cursor(); cursor.execute("UPDATE TENANT_TECHNICIAN SET deleted_at=NOW(),updated_at=NOW() WHERE id=%s AND client_id=%s AND deleted_at IS NULL",(technician_id,client_id)); result=cursor.rowcount; conn.commit();cursor.close();return result
    def update_signature(self, technician_id, client_id, key, content_type, size, conn):
        cursor=conn.cursor();cursor.execute("UPDATE TENANT_TECHNICIAN SET signature_object_key=%s,signature_content_type=%s,signature_size_bytes=%s,signature_updated_at=NOW(),updated_at=NOW() WHERE id=%s AND client_id=%s AND deleted_at IS NULL",(key,content_type,size,technician_id,client_id));conn.commit();cursor.close()
    def owned_ids(self, ids, client_id, conn):
        if not ids:return []
        tokens=', '.join(['%s']*len(ids));cursor=conn.cursor(dictionary=True);cursor.execute(f"SELECT id FROM TENANT_TECHNICIAN WHERE client_id=%s AND deleted_at IS NULL AND id IN ({tokens})",(client_id,*ids));rows=[x['id'] for x in cursor.fetchall()];cursor.close();return rows
