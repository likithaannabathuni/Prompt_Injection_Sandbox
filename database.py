import sqlite3
import os


DATABASE_PATH = "data/prompt_sandbox.db"


def get_connection():

    os.makedirs(
        "data",
        exist_ok=True
    )

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    # =========================================
    # USERS TABLE
    # =========================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
        """
    )


    # =========================================
    # TEST RESULTS TABLE
    # =========================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS test_results (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER NOT NULL,

            prompt_text TEXT NOT NULL,

            llm_response TEXT,

            detection_result TEXT,

            risk_score REAL,

            model TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (user_id)
                REFERENCES users(id)

        )
        """
    )


    conn.commit()

    conn.close()


initialize_database()