from src.model.app_user import AppUser


class AppUserRepository:

    def find_by_email(self, email: str, conn):
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM APP_USER WHERE email = %s"

        cursor.execute(sql, (email,))

        user = cursor.fetchone()

        cursor.close()

        return AppUser(**user) if user else None

    def find_by_id(self, id: str, conn):
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM APP_USER WHERE id = %s"

        cursor.execute(sql, (id,))

        user = cursor.fetchone()

        cursor.close()

        return AppUser(**user) if user else None

    def create(self, user: AppUser, conn):
        cursor = conn.cursor()

        sql = "INSERT INTO APP_USER (id, email, password, name, document, id_client, created_at, updated_at) VALUES (uuid(), %s, %s, %s, %s, %s, NOW(), NOW())"

        cursor.execute(sql, (user.email, user.password, user.name, user.document, user.id_client))

        user.id = cursor.lastrowid

        cursor.close()

        return user
