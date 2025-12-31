import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

def init_database():
    try:
        # Check if password was loaded correctly
        if not DB_PASS:
            print("❌ Error: DB_PASS is missing. Check your .env file.")
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

        # SQL to create the table
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
        print("\nTroubleshooting Tip: If it says 'timeout', check your AWS Security Group.")

if __name__ == "__main__":
    init_database()         