import psycopg
from psycopg import sql

def setup_db():
    try:
        # Connect to default 'postgres' database
        # Try connecting as current user first
        conn = psycopg.connect("dbname=postgres", autocommit=True)
    except Exception as e:
        print(f"Failed to connect as current user: {e}")
        try:
            # Try connecting as postgres user
            conn = psycopg.connect("dbname=postgres user=postgres", autocommit=True)
        except Exception as e2:
            print(f"Failed to connect as postgres user: {e2}")
            return

    cur = conn.cursor()
    
    # Create user if not exists
    try:
        cur.execute("CREATE USER yfe WITH PASSWORD 'yfe_dev_pass';")
        print("User 'yfe' created.")
    except psycopg.errors.DuplicateObject:
        print("User 'yfe' already exists.")
    except Exception as e:
        print(f"Error creating user: {e}")

    # Create database if not exists
    try:
        cur.execute("CREATE DATABASE yfe_db OWNER yfe;")
        print("Database 'yfe_db' created.")
    except psycopg.errors.DuplicateDatabase:
        print("Database 'yfe_db' already exists.")
    except Exception as e:
        print(f"Error creating database: {e}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_db()
