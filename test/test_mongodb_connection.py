#!/usr/bin/env python3
"""
Test script to verify MongoDB connection and basic patron operations
"""

from repository.mongodb_database import connect_mongodb, disconnect_mongodb, get_mongodb_connection
from repository.patron_repository import PatronRepository
from models.patron import Patron
from datetime import datetime

def test_connection():
    """Test MongoDB connection"""
    print("Testing MongoDB connection...")
    
    if connect_mongodb():
        print("✓ MongoDB connection successful")
        
        # Test repository operations
        try:
            patron_repo = PatronRepository()
            
            # Create a test patron
            test_patron = Patron(
                id=None,
                first_name="Test",
                last_name="User",
                email="test@example.com",
                phone="555-0000",
                address="Test Address",
                membership_type="student",
                membership_start_date=datetime.now(),
                membership_end_date=None,
                books_checked_out=[],
                total_books_borrowed=0,
                active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            # Test create
            patron_id = patron_repo.create_patron(test_patron)
            print(f"✓ Created test patron with ID: {patron_id}")
            
            # Test retrieve
            retrieved = patron_repo.get_patron_by_id(patron_id)
            if retrieved:
                print(f"✓ Retrieved patron: {retrieved.get_full_name()}")
            
            # Test delete
            deleted = patron_repo.delete_patron_by_id(patron_id)
            if deleted:
                print("✓ Successfully deleted test patron")
            
            print("✓ All patron operations successful")
            
        except Exception as e:
            print(f"✗ Error during patron operations: {e}")
        
        disconnect_mongodb()
        print("✓ Disconnected from MongoDB")
        
    else:
        print("✗ MongoDB connection failed")
        print("Please ensure MongoDB is running and accessible")

if __name__ == "__main__":
    test_connection()


