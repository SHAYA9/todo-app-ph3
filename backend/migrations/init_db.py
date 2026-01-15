"""Initialize database with tables"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from database.config import init_db

if __name__ == "__main__":
    print("Creating database tables...")
    init_db()
    print("✅ Database initialized successfully!")