import os
import psycopg2

def get_db_connection():
    """
    Establishes a connection to the PostgreSQL database using environment variables.
    """
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "Postgres")
    )
    return conn
    print(conn)

# Example usage (for testing)
if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("Connected to PostgreSQL database successfully!")
        # You can perform database operations here
        conn.close()
        print("Connection closed.")
    except Exception as e:
        print(f"Error connecting to database: {e}")
        print("Make sure PostgreSQL is running and environment variables are set correctly.") 

