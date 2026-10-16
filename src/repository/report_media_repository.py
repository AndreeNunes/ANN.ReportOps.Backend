class ReportMediaRepository:
    def get_report_media(self, report_reference_id, conn):
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id, media_type AS type, media_group AS `group`, object_key, content_type,
                   size_bytes, note, created_at, updated_at
            FROM REPORT_MEDIA
            WHERE report_reference_id = %s
            ORDER BY media_type, created_at
            """,
            (report_reference_id,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_manifests(self, reference_ids, conn):
        if not reference_ids:
            return {}
        cursor = conn.cursor(dictionary=True)
        placeholders = ", ".join(["%s"] * len(reference_ids))
        cursor.execute(
            f"SELECT report_reference_id, id, media_type AS type, media_group AS `group`, "
            f"object_key, content_type, size_bytes, note, updated_at "
            f"FROM REPORT_MEDIA WHERE report_reference_id IN ({placeholders})",
            tuple(reference_ids),
        )
        result = {}
        for row in cursor.fetchall():
            reference_id = row.pop("report_reference_id")
            if hasattr(row.get("updated_at"), "isoformat"):
                row["updated_at"] = row["updated_at"].isoformat()
            result.setdefault(reference_id, []).append(row)
        cursor.close()
        return result

    def lock_report(self, report_reference_id, conn):
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM REPORT WHERE id_reference = %s FOR UPDATE",
            (report_reference_id,),
        )
        cursor.fetchone()
        cursor.close()

    def foreign_media_ids(self, ids, report_reference_id, conn):
        if not ids:
            return []
        cursor = conn.cursor(dictionary=True)
        placeholders = ", ".join(["%s"] * len(ids))
        cursor.execute(
            f"SELECT id FROM REPORT_MEDIA WHERE id IN ({placeholders}) "
            f"AND report_reference_id <> %s",
            (*ids, report_reference_id),
        )
        rows = cursor.fetchall()
        cursor.close()
        return [row["id"] for row in rows]

    def replace_report_media(self, report_reference_id, media, conn):
        cursor = conn.cursor()
        ids = [item.id for item in media]
        if ids:
            placeholders = ", ".join(["%s"] * len(ids))
            cursor.execute(
                f"DELETE FROM REPORT_MEDIA WHERE report_reference_id = %s "
                f"AND id NOT IN ({placeholders})",
                (report_reference_id, *ids),
            )
        else:
            cursor.execute(
                "DELETE FROM REPORT_MEDIA WHERE report_reference_id = %s",
                (report_reference_id,),
            )
        if media:
            cursor.executemany(
                """
                INSERT INTO REPORT_MEDIA (
                    id, report_reference_id, media_type, media_group, object_key,
                    content_type, size_bytes, note, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(6), NOW(6))
                ON DUPLICATE KEY UPDATE
                    media_type = VALUES(media_type),
                    media_group = VALUES(media_group),
                    object_key = VALUES(object_key),
                    content_type = VALUES(content_type),
                    size_bytes = VALUES(size_bytes),
                    note = VALUES(note)
                """,
                [
                    (
                        item.id, report_reference_id, item.type, item.group,
                        item.object_key, item.content_type, item.size_bytes, item.note,
                    )
                    for item in media
                ],
            )
        conn.commit()
        cursor.close()
