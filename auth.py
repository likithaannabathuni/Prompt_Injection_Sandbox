import hashlib

from database import get_connection


def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
            """,
            (
                username,
                password_hash
            )
        )

        conn.commit()

        return True

    except Exception:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id, username
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            password_hash
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return user

    return None