from flask import Flask
from flask_httpauth import HTTPBasicAuth
import mysql.connector
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = "keinth123"

auth = HTTPBasicAuth()
USER_DATA_FILE = "users.json"

# Database Connection Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'elective'
}

def get_db_connection():
    """Create and return a database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL Database: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Execute a database query with optional parameters"""
    connection = get_db_connection()
    if not connection:
        return None

    try:
        cursor = connection.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount
        
        cursor.close()
        connection.close()
        return result
    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        if connection:
            connection.close()
        return None
    

def load_users():
    """Load users from JSON file"""
    try:
        with open(USER_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USER_DATA_FILE, "w") as file:
        json.dump(users, file)

users = load_users()