import sqlite3
import bcrypt  # Ensure bcrypt is installed


def register_user(username, password):
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully.")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect('budget_tracker.db')
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM Users WHERE username = ?", (username,))
    result = cursor.fetchone()

    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
        print("Login successful.")
        return True
    else:
        print("Invalid credentials.")
        return False
