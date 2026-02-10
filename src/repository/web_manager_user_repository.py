from src.model.web_manager_user import WebManagerUser


class WebManagerUserRepository:
    def find_by_email(self, email: str, conn):
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM WEB_MANAGER_USER WHERE email = %s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        cursor.close()
        return WebManagerUser(**user) if user else None

    def create(self, user: WebManagerUser, conn):
        cursor = conn.cursor()
        sql = "INSERT INTO WEB_MANAGER_USER (id, name, email, password, id_client, date_entered) VALUES (%s, %s, %s, %s, %s, NOW())"
        cursor.execute(sql, (user.id, user.name, user.email, user.password, user.id_client))
        cursor.close()
        return user

