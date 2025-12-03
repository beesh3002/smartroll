from flask import Blueprint, request, jsonify
import sqlite3
import os

# Create a new blueprint for signup
signup_bp = Blueprint("signup", __name__, url_prefix="/api")

# Database file path
DB_PATH = "instance/database.db"

# Ensure users table exists
def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database when this file is imported
init_db()


@signup_bp.route("/signup", methods=["POST"])
def signup():
    """Handles user registration requests from the Flutter app."""
    data = request.get_json() or {}

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    email = data.get("email")
    password = data.get("password")

    # Validate required fields
    if not all([first_name, last_name, email, password]):
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Ensure the users table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                email TEXT UNIQUE,
                password TEXT
            )
        ''')

        # Check if the email is already registered
        cursor.execute("SELECT id FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            conn.close()
            return jsonify({"status": "error", "message": "Email already exists"}), 409

        # Insert the new user
        cursor.execute(
            "INSERT INTO users (first_name, last_name, email, password) VALUES (?, ?, ?, ?)",
            (first_name, last_name, email, password)
        )
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "User registered successfully"}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

