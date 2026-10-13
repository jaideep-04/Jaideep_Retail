import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Get values from .env
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_TYPE = os.getenv('DB_TYPE')

print("=" * 80)
print("DATABASE CONNECTION TEST (MySQL)")
print("=" * 80)

print("\n✓ Configuration Loaded from .env:")
print(f"  Host: {DB_HOST}")
print(f"  Port: {DB_PORT}")
print(f"  Database: {DB_NAME}")
print(f"  User: {DB_USER}")
print(f"  Type: {DB_TYPE}")

# Try to connect
print("\n⏳ Testing connection...")

try:
    from sqlalchemy import create_engine
    
    # Build connection string for MySQL
    DATABASE_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    print(f"\nConnection String: {DB_TYPE}://{DB_USER}:****@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    
    # Try to connect
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        print("\n✅ SUCCESS! MySQL Database connection works!")
        print("\n✓ You can now:")
        print("  - Run ETL pipeline")
        print("  - Create database tables")
        print("  - Load data")
        
except Exception as e:
    print(f"\n❌ ERROR: Connection failed!")
    print(f"\nError message: {e}")
    print("\nTroubleshooting:")
    print("  1. Is MySQL running? (Check Windows Services)")
    print("  2. Is the password correct in .env?")
    print("  3. Does the database exist? (Run: mysql -u root -p)")
    print("  4. Check .env file values")
    print("  5. Is pymysql installed? (Run: pip install pymysql)")

print("\n" + "=" * 80)