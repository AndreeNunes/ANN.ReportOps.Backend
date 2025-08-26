from src.model.app_user import AppUser


class AppUserRepository:

    def find_by_email(self, email: str, conn):
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT * FROM APP_USER WHERE email = %s"

        cursor.execute(sql, (email,))

        user = cursor.fetchone()

        cursor.close()

        return AppUser(**user) if user else None

    def create(self, user: AppUser, conn):
        cursor = conn.cursor()

        sql = "INSERT INTO APP_USER (id, email, password, name, document, client_id) VALUES (uuid(), %s, %s, %s, %s, %s)"

        cursor.execute(sql, (user.email, user.password, user.name, user.document, user.client_id))

        user.id = cursor.lastrowid

        cursor.close()

        return user
