import psycopg2
import os  # <--- Added this to read environment variables
from psycopg2 import sql

# --- CONFIGURATION ---
DB_HOST = os.environ.get("DB_HOST", "tadawul-db.c8xyiyy40mmd.us-east-1.rds.amazonaws.com")
DB_NAME = os.environ.get("DB_NAME", "tadawul")
DB_USER = os.environ.get("DB_USER", "postgres")

# 🔒 SAFE: No real password here!
DB_PASS = os.environ.get("DB_PASS", "PLACEHOLDER_PASS")

def init_database():
    try:
        # Check if we are using the placeholder (Safety check)
        if DB_PASS == "PLACEHOLDER_PASS":
            print("⚠️  Cannot connect: Password is a placeholder. Set DB_PASS to run.")
            return

        print("1. Connecting to AWS RDS...")
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            port=5432
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("   ✅ Connected successfully!")

        # Define the table structure
        create_table_query = """
        CREATE TABLE IF NOT EXISTS daily_prices (
            symbol VARCHAR(20) NOT NULL,
            date DATE NOT NULL,
            open DECIMAL(10, 2),
            high DECIMAL(10, 2),
            low DECIMAL(10, 2),
            close DECIMAL(10, 2),
            volume BIGINT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (symbol, date)
        );
        """

        print("2. Creating table 'daily_prices'...")
        cursor.execute(create_table_query)
        print("   ✅ Table created (or already exists)!")

        cursor.close()
        conn.close()
        print("\n🎉 Database is ready for data!")

    except Exception as e:
        print("\n❌ Connection Failed:")
        print(e)
        print("\nTroubleshooting Tip: If it says 'timeout', check your Security Group allows your IP.")

if __name__ == "__main__":
    init_database()