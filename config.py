import psycopg2
from psycopg2.extras import RealDictCursor

# PostgreSQL configuration
DB_HOST = "localhost"
DB_NAME = "whatsapp2web_db"
DB_USER = "postgres"
DB_PASSWORD = "root"  # Replace with the password you used
DB_PORT = 5432

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT,
            cursor_factory=RealDictCursor  # returns results as dictionaries
        )
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None
