import sqlite3


def test_connection():
    connection = sqlite3.connect("data/rugby.db")
    print("Database connected successfully")
    connection.close()


test_connection()
