# app/migrate_to_multicompany.py

"""
Database Migration Script
Migrates from single-company to multi-company system.
"""

import sys
import os

# Add parent directory to path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base
from app.models.user import User
from app.models.company import Company
from app.models.company_member import CompanyMember
from app.models.invitation import Invitation

def migrate_database():
    """
    Drop old tables and create new schema.
    
    WARNING: This will delete all existing data!
    For production, use proper migrations (Alembic).
    """
    print("=" * 50)
    print("🔄 Migrating to Multi-Company System")
    print("=" * 50)
    
    # Drop all existing tables
    print("\n⚠️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    # Create new tables
    print("✅ Creating new tables...")
    Base.metadata.create_all(bind=engine)
    
    print("\n✅ Migration complete!")
    print("\nNew tables created:")
    print("  - users")
    print("  - companies")
    print("  - company_members")
    print("  - invitations")
    print("=" * 50)

if __name__ == "__main__":
    migrate_database()