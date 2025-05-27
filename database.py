import mysql.connector
from mysql.connector import Error


def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="", database="db_ta_kelompok7"
        )
        if conn.is_connected():
            print("Berhasil tersambung ke database!")
            return conn
    except Error as e:
        print(f"Gagal tersambung ke database: {e}")
        return None


if __name__ == "__main__":
    connect_db()
